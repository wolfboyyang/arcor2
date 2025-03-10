import inspect
import logging
import os
import subprocess as sp
import tempfile
from typing import Iterator

import pytest

from arcor2.clients import project_service, scene_service
from arcor2.data.events import Event
from arcor2.data.rpc.common import TypeArgs
from arcor2.helpers import find_free_port
from arcor2_arserver_data import events, rpc
from arcor2_arserver_data.client import ARServer, get_id
from arcor2_execution_data import EVENTS as EXE_EVENTS
from arcor2_logger.object_types.logging_test_object import LoggingTestObject
from arcor2_logger.object_types.logging_test_robot import LoggingTestRobot

LOGGER = logging.getLogger(__name__)


_arserver_port: int = 0


def log_proc_output(out: tuple[bytes, bytes]) -> None:

    for line in out[0].decode().splitlines():
        LOGGER.error(line)


def finish_processes(processes) -> None:

    for proc in processes:
        proc.terminate()
        proc.wait()
        log_proc_output(proc.communicate())


@pytest.fixture()
def start_processes() -> Iterator[None]:

    global _arserver_port

    _arserver_port = find_free_port()

    with tempfile.TemporaryDirectory() as tmp_dir:

        my_env = os.environ.copy()

        project_port = find_free_port()
        project_url = f"http://0.0.0.0:{project_port}"
        my_env["ARCOR2_PROJECT_SERVICE_URL"] = project_url
        my_env["ARCOR2_PROJECT_SERVICE_MOCK_PORT"] = str(project_port)
        project_service.URL = project_url

        scene_port = find_free_port()
        scene_url = f"http://0.0.0.0:{scene_port}"
        my_env["ARCOR2_SCENE_SERVICE_URL"] = scene_url
        my_env["ARCOR2_SCENE_SERVICE_MOCK_PORT"] = str(scene_port)
        scene_service.URL = scene_url

        my_env["ARCOR2_EXECUTION_URL"] = f"ws://0.0.0.0:{find_free_port()}"
        my_env["ARCOR2_PROJECT_PATH"] = os.path.join(tmp_dir, "packages")

        my_env["ARCOR2_ARSERVER_PORT"] = str(_arserver_port)

        processes = []

        for cmd in (
            "./src.python.arcor2_mocks.scripts/mock_project.pex",
            "./src.python.arcor2_mocks.scripts/mock_scene.pex",
            "./src.python.arcor2_execution.scripts/execution.pex",
        ):
            processes.append(sp.Popen(cmd, env=my_env, stdout=sp.PIPE, stderr=sp.STDOUT))

        scene_service.wait_for(60)

        # it may take some time for project service to come up so give it some time
        for _ in range(3):
            upload_proc = sp.Popen(
                "./src.python.arcor2_logger.scripts/upload_objects.pex", env=my_env, stdout=sp.PIPE, stderr=sp.STDOUT
            )
            ret = upload_proc.communicate()
            if upload_proc.returncode == 0:
                log_proc_output(ret)
                break
        else:
            raise Exception("Failed to upload objects.")

        LOGGER.info(f"Starting ARServer listening on port  {_arserver_port}.")

        arserver_proc = sp.Popen(
            "./src.python.arcor2_arserver.scripts/arserver.pex", env=my_env, stdout=sp.PIPE, stderr=sp.STDOUT
        )

        processes.append(arserver_proc)
        assert arserver_proc.stdout is not None

        while True:
            line = arserver_proc.stdout.readline().decode().strip()
            LOGGER.info(line)
            if not line or (") initialized." in line):  # TODO this is not ideal
                break

        if arserver_proc.poll():
            finish_processes(processes)
            raise Exception("ARServer died.")

        yield None

        finish_processes(processes)


def ars_connection_str() -> str:
    return f"ws://0.0.0.0:{_arserver_port}"


# TODO refactor this into _data packages
event_mapping: dict[str, type[Event]] = {evt.__name__: evt for evt in EXE_EVENTS}

modules = []

for _, mod in inspect.getmembers(events, inspect.ismodule):
    modules.append(mod)

for mod in modules:
    for _, cls in inspect.getmembers(mod, inspect.isclass):
        if issubclass(cls, Event):
            event_mapping[cls.__name__] = cls


@pytest.fixture()
def ars() -> Iterator[ARServer]:

    with ARServer(ars_connection_str(), timeout=30, event_mapping=event_mapping) as ws:
        yield ws


def test_objects(start_processes: None, ars: ARServer) -> None:

    assert isinstance(ars.get_event(), events.c.ShowMainScreen)

    res = ars.call_rpc(rpc.o.GetObjectTypes.Request(get_id()), rpc.o.GetObjectTypes.Response)
    assert res.result
    assert res.data is not None

    assert {obj.type for obj in res.data if not obj.built_in} == {LoggingTestObject.__name__, LoggingTestRobot.__name__}

    for obj in res.data:
        assert not obj.disabled, f"ObjectType {obj.type} disabled. {obj.problem}"

        actions = ars.call_rpc(rpc.o.GetActions.Request(get_id(), TypeArgs(obj.type)), rpc.o.GetActions.Response)
        assert actions.result
        assert actions.data is not None

        for act in actions.data:
            assert act.disabled == (act.problem is not None)
            assert not act.disabled, f"Action {act.name} of {obj.type} disabled. {act.problem}"

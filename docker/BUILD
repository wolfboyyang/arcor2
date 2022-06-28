file(name="start-arserver", source="start-arserver.sh")
file(name="start-build", source="start-build.sh")
file(name="start-calibration", source="start-calibration.sh")
file(name="start-dobot", source="start-dobot.sh")
#file(name="start-execution-proxy", source="start-execution-proxy.sh")
file(name="start-execution", source="start-execution.sh")
file(name="start-fanuc", source="start-fanuc.sh")
file(name="start-mocks", source="start-mocks.sh")

docker_image(
    name="dist-base",
    repository="arcor2/arcor2_dist_base",
    source="Dockerfile-dist-base",
    image_tags=["{build_args.VERSION}"],
)

docker_image(
    name="arserver",
    repository="arcor2/arcor2_arserver",
    source="Dockerfile-arserver",
    dependencies=[":start-arserver", "src/python/arcor2_arserver/scripts:arserver"],
    image_tags=["{build_args.VERSION}"],
)

docker_image(
    name="build",
    repository="arcor2/arcor2_{name}",
    source="Dockerfile-build",
    dependencies=[":start-build", "src/python/arcor2_build/scripts:build"],
    image_tags=["{build_args.VERSION}"],
)

docker_image(
    name="execution",
    repository="arcor2/arcor2_{name}",
    source="Dockerfile-execution",
    dependencies=[":start-execution", "src/python/arcor2_execution/scripts:execution"],
    image_tags=["{build_args.VERSION}"],
)

docker_image(
    name="calibration",
    repository="arcor2/arcor2_{name}",
    source="Dockerfile-calibration",
    dependencies=[":start-calibration", "src/python/arcor2_calibration/scripts:calibration"],
    image_tags=["{build_args.VERSION}"],
)

docker_image(
    name="dobot",
    repository="arcor2/arcor2_{name}",
    source="Dockerfile-dobot",
    dependencies=[":start-dobot", "src/python/arcor2_dobot/scripts:dobot"],
    image_tags=["{build_args.VERSION}"],
)

docker_image(
    name="mocks",
    repository="arcor2/arcor2_{name}",
    source="Dockerfile-mocks",
    dependencies=[":start-mocks",
                  "src/python/arcor2_mocks/scripts:mock_project",
                  "src/python/arcor2_mocks/scripts:mock_scene",
                  ],
    image_tags=["{build_args.VERSION}"],
)

docker_image(
    name="upload_fit_demo",
    repository="arcor2/arcor2_{name}",
    source="Dockerfile-upload-fit-demo",
    dependencies=["src/python/arcor2_fit_demo/scripts:upload_objects"],
    image_tags=["{build_args.VERSION}"],
)
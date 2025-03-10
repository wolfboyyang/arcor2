# Changelog

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),

## [0.23.1] - 2022-02-17

### Added

- Simple collision checking.
  - Related dataclasses were added.
  - New function in `scene_service` client.

## [0.23.0] - 2022-01-25

### Changed

- **BREAKING**: `ActionStateBefore` event updated.
  - Properties `action_id` and `parameters` are now optional.
  - New optional property `action_point_ids`. 
- Switched to Python 3.9, updated dependencies. 

## [0.22.0] - 2021-10-25

### Changed

- New abstract base class `VirtualCollisionObject`.
  - Meant as a base for 'dumb' collision objects, with primitive models, without any functionality, e.g. for safety 'walls' around the cell.
- `ActionMetadata` updated.
  - Removed useless properties (`blocking`, `blackbox`).
  - Added a new property `hidden` (UIs shall silently ignore those actions).
- Dropped support for `RelativePose` action parameter type.
- Handle all errors when importing stuff (`import_type_def`).
  - This is needed for instance in case of obsolete ObjectTypes.
  - ...when e.g. parameters of `ActionMetadata` were changed.
  - Otherwise outdated OT might raise `TypeError` or similar exceptions.
- New (optional) properties added to `BareActionPoint` (compatibility with Project service 0.14.0 or newer).
- Added `FlowActions` ObjectType, providing `is_first_pass` action which is useful to perform the initialization step.

### Fixed

- Action point transformations (reparenting).
  - When AP1 from `object -> AP1 -> AP2` was made global, AP2 was not updated properly.
  - When AP1 was made relative again, AP2 was again not updated.

## [0.21.0] - 2021-09-07

### Changed

- Added `Robot` specific exception `KinematicsException`.
  - So far used to give more precise error messages.
- `ProjectParameter` now derives from `Parameter`.
- `CachedScene` now caches ObjectTypes used in a scene.
- Logs are now colored.
- `Project` now has optional `project_objects_ids` property (not used at the moment).

### Fixed

- Make sure that `Pose` contain only floats.
  - When any value is e.g. np.float64, `orjson` complains.
  - Because of this, `to_dict` methods of `Position` and `Orientation` are overridden.
- Typo in URL within `get_models` of `project_service` client.
- Missing sleep in `wait_for` of `scene_service` client.

## [0.20.0] - 2021-08-05

### Changed

- Object hierarchy modified.
  - `GenericWithPose` now can't have a collision model.
  - A new `CollisionObject` must have collision model.
- `Robot` base class API changed.
  - Parameter `linear` was added to `move_to_pose`.
    - A robot not supporting linear movements should raise exception when `linear==True`.  
  - Parameter `include_gripper` was added to `robot_joints`.
    - By default, the method should return only arm's joints.
    - With the parameter set, the list should contain also gripper joints.
    - This is needed for visualization of grippers.
    - Makes only sense (so far) when gripper is part of URDF.
- Scene/Project clients now log underlying error messages.

### Fixed

- `rest` module now encodes body data as utf-8. 


## [0.19.0] - 2021-07-29

### Changed

- Support for multi arm robots.
  - New base class `MultiArmRobot`.
  - Its methods have an additional `arm_id` parameter.
  - There is a method to get arm IDs.
  - Relevant ARServer RPCs were extended with `arm_id`.
  - `ProjectRobotJoints` model now also contains `arm_id`.
  - There is `DummyMultiArmRobot` ObjectType for testing purposes.
- `CachedProject`: `constants` renamed to `parameters`.
- `Generic`: `INIT_PRIORITY` removed as useless.
- `GenericWithPose`: do not delete collision models in `cleanup`.
  - Collision models are removed by the Scene service on `stop`.
- Usage of `orjson` in `arcor2/json` and for dataclasses.
  - 40% speedup for serialization.
  - 80% speedup for deserialization.
  - Tested on `Project` dataclass.
- Compatibility with Project service 0.10.0.
- Compatibility with Scene service 0.5.0.  
- Uploading of meshes associated to ObjectTypes.
  - Parameter `file_to_upload` was added to `upload_def`.

### Fixed

- Correct default port for Project service (10000).

## [0.18.0] - 2021-06-14

### Changed
- Modules `package` and `resources` moved to `arcor2_execution_data`.

## [0.17.0] - 2021-06-11

### Changed
- Project service client updated to API version 0.8.0.
- `ARCOR2_PERSISTENT_STORAGE_URL` renamed to `ARCOR2_PROJECT_SERVICE_URL`.  
- Dependencies updated.

## [0.16.0] - 2021-05-21

### Changed
- Objects initialization order (`Resources`):
  - Object initialization order can be set using class-level `INIT_PRIORITY` variable.
  - The higher priority, the sooner are objects of that type initialized.
  - Objects are initialized serially.
- `CachedProject` has new methods to deal with hierarchy (`get_by_id`, `get_parent_id`, `childs`).
- Project service client updated to be compatible with version 0.7.0.
- Added a custom `json` module.
  - Wraps the standard json module, so it might be easier to replace it in the future.
  - Provides type annotations.
  - Raises a custom exception based on `Arcor2Exception`.

### Fixed
- Handling of context manager arguments in `Resources`.

## [0.15.0] - 2021-04-20

### Changed
- REST client now handles all codes >= 400 as errors.

## [0.14.1] - 2021-04-19

### Fixed
- Save and import of ObjectType was randomly failing because of [race condition](https://docs.python.org/3.8/library/importlib.html#importlib.machinery.FileFinder).

## [0.14.0] - 2021-03-30

### Changed
- Improved code for transforming poses.
- Use monkey patching instead of custom released version of dataclasses_jsonschema.
- Switched to builtin ast module instead of horast - much faster builds, etc.
- Added states `Stopping` and `Pausing` to `PackageState.Data.StateEnum`.
  - This is because it may take some time to pause or stop a package.
  - Other operations (as e.g. resume) are almost instant.

### Fixed
- `Resources` are now not sending `KeyboardInterrupt` as event.
- `import_type_def` now provides better error messages when import fails.
- Save and import of ObjectType was randomly failing.

## [0.13.0] - 2021-03-15

### Changed
- IDs (uuid) are now generated within the respective classes.
  - If necessary, ID can be still provided from outside as before.
  - IDs are prefixed so developers can easily check type of an object from its ID.
  - Prefix always start with a character.

### Fixed
- Composite actions are now properly handled by the `@action` decorator.

## [0.12.1] - 2021-03-08

### Fixed
- `Pose` parameter plugin fixed to generate correct code in a case when action on action point A uses orientation from action point B.

## [0.12.0] - 2021-03-03

### Fixed
- Parameter plugins now return copy of the parameter in order to prevent changes in the project if the value is modified e.g. within an action.
- Method `update_project_sources` of the Project service client was fixed.

### Changed
- Flask-based apps now don't log each API call by default.
  - It can be turned on by setting `ARCOR2_REST_API_DEBUG`.
- The `rest` module has a new exception type RestHttpException for getting HTTP error codes.
- `is_valid_identifier` now behaves the same as `is_valid_type`, it does not insist on convention (PascalCase vs snake_case) and provides concrete error messages.
- `Robot` API now has `safe` parameter.
- `Robot` now has API for hand teaching mode.  
- Line length of generated code changed from 80 to 120.

## [0.11.1] - 2021-02-09

### Fixed
- `@action` decorator fixed.
- `KeyError` was raised when `an` parameter was not given to an action.
- This only happened in the "manual" script writing scenario and when `patch_object_actions` was used.

## [0.11.0] - 2021-02-08

### Changed
- Explicit action parameters.
  - `Resources` class now do not need to deal with parameters.
  - Update of ObjectTypes (all actions now have the mandatory `an` parameter).
- `CurrentAction` removed, `ActionState` divided into `ActionStateBefore` and `ActionStateAfter`.
- New module with shared code for Flask-based apps.
- Updates of 3rd party dependencies.
- WS server now logs too long RPCs. 
  - Max. duration could be configured using `ARCOR2_MAX_RPC_DURATION`.

### Fixed
- At a startup, the main script now checks if the scene is running before attempt to stop it.
- `image_from_str` function fixed.

## [0.10.0] - 2020-12-14

### Changed
- `action` decorator now handles outputs of actions.
- `CachedProject` has new methods for handling project logic.
- `ActionState` event now contains action results.
- New built-in ObjectTypes `RandomActions`.
- Parameter plugins slightly reworked, some new helper functions.
- If a robot has URDF, it is zipped and uploaded to the Project service).
  - ...as a mesh file, which is workaround for missing storage of URDF models.
- Scene service client updated to support version 0.4.0.
- New built-in abstract ObjectType `Camera`.
- Initial support for loading of URDF files.
- Some first tests for parameter plugins were added.

## [0.9.2] - 2020-10-30

### Fixed
- `parse` function now also catches `ValueError` exception.
-  `check_object_type` now tries to parse whole module instead of just source of the class itself.

### Changed
- `Robot` base class now have methods for IK/FK.
- It is possible to use `==` on `Position` instances.

## [0.9.1] - 2020-10-19

### Fixed
- package_version was ignoring `package` argument

## [0.9.0] - 2020-10-16

### Changed
- Scene client updated for Scene 0.3.0.
- Exceptions refactored (BREAKING).
  - Arcor2Exception no longer has `message` property
  - There is a new package arcor2/exceptions.
  - Clients using `handle` decorator now have specific error messages defined.
  - Previously generated execution packages will become broken as `print_exception` function was moved 
- Loggers are now created using functions from `logging` module.
- `rest` module rewritten (BREAKING).
  - Now there is only one method `call` which takes http method as an argument.
  - There is `ARCOR2_REST_DEBUG` environment variable. When set, debugging logs are turned on.

### Fixed
- JSON containing only boolean value was not handled properly by `arcor2.rest` module.


## [0.8.0] - 2020-09-24
### Changed
- Reorganisation of the repository - switched to monorepo based on [Pants](https://www.pantsbuild.org/docs/welcome-to-pants). The code was divided into more packages (that can be separatelly relased) within one repository.
- Tests now run on GitHub instead of CircleCi.
- Unification of objects and services
  - There is ```Generic``` base class for objects without pose, ```GenericWithPose``` for objects with pose and ```Robot``` class that should be base class for every robot.
- Integration of scene service (0.2.0).
- @action decorator is now added automatically in the run-time.
- ```Orientation``` dataclass now performs quaternion normalization in ```__post_init__```.
- ```Robot``` base class now has ```_move_lock``` mutex to ensure that only one move-action is called at the time.

## [0.8.0rc2] - 2020-09-16

## [0.8.0rc1] - 2020-09-15

## [0.8.0b8] - 2020-08-21
### Fixed
- Some robot-related issues fixed

## [0.8.0b7] - 2020-08-12
### Changed
- Scene service client: 'upsert_collision' now has optional 'mesh_parameters': parameter.

## [0.8.0b6] - 2020-08-03
### Changed
- New logic representation
- Unification of objects and services
- Integration of scene service

## [0.7.1] - 2020-07-15
### Fixed
- Fix of broken python package arcor2 0.7.0

## [0.7.0] - 2020-07-15
### Changed

- ARServer: new RPC 'TemporaryPackage'
- ARServer: RPC ObjectTypesChangedEvent renamed to ChangedObjectTypesEvent, now contains changed ObjectTypes meta instead of just type names
- ARServer: ShowMainScreenEvent.
- Package name added to PackageInfoEvent
- ARServer now compares its API_VERSION with API_VERSION of the Execution.
- ARServer: ShowMainScreenEvent will now not contain 'highlight' when sent to a newly connected UI.
- AP can now have another AP as parent
- rest: OptionalData now may contain list of primitive type.
- Execution: PackageStateEvent now contains package_id
- Execution: added 'executed' to PackageMeta

## [0.6.0] - 2020-06-19
### Changed

- Build/Execution proxy: allow port change using env. var.
- ARServer: RenameScene RPC now checks if scene name is unique and 'dry_run' works.
- ARServer: ListScenes/ListProjects now contain 'modified'.
- ARServer: DeleteObjectType RPC added.
- @action decorator is now compatible with Windows.
- Service class now has 'cleanup' method which is called when scene is closed or when script ends. Call of 'cleanup' can be disabled by 'export ARCOR_CLEANUP_SERVICES=False' - this is particularly useful when running the script manually again and again.
- Cleanup method for ObjectTypes.

## [0.5.1] - 2020-06-04
### Fixed
- ignoring check of return parameters
- allowing list of strings as request body

## [0.5.0] - 2020-06-01
### Changed
- ARServer container need to setup new env variable using docker-compose -> ARCOR2_DATA_PATH=/root/data
- ListProjects RPC now gets projects in parallel.
- dry_run parameter for selected RPCs
- EEF pose/robot joints streaming
- OpenScene, OpenProject, SceneClosed, ProjectClosed events.
- Execution proxy: use persistent websocket connection.
- SceneCollisionsEvent merged into PackageInfoEvent
- ARServer: RPC to cancel action execution.
- Execution package now contains package.json with its metadata. Execution service now supports renaming of packages.

## [0.4.3] - 2020-05-22
### Changed
- added support for CORS

## [0.4.2] - 2020-04-27
### Fixed
- Fix of functions to transform relative poses to absolute and vice versa

## [0.4.1] - 2020-04-22
### Added
- New RPCs for getting robot joints and effector pose
- New RPC to get IDs of EE and suctions
- Added pivot enum for UpdateObjectPoseUsingRobot

### Fixed
- Fix of remove action RPC
- Another fixes


## [0.4.0] - 2020-04-17
### Changed
- Complete redesign of RPC for ARClients (AREditor atm)
- Documentation of execution and build API
- Support for project service 0.2.0
- New and updated events
- Enhanced error messages
- Create (global) session to enable reuse of connections.

## [0.3.0] - 2020-03-24
### Changed
- Renamed RobotJoints to ProjectRobotJoints and ModelTypeEnum to Model3dType
- Added new services for Time and Logic related actons
- Added boolean parameter plugin
- Description, returns and origins fields marked as optional
- New event - ActionResult
- Separated script enabling discovery through UDP broadcast
- Support for list params
- Services and Action objects are now marked as disabled when some problem occured and error message is passed to GUI (previously such services/objects were ignored)
- Services with no configuration are disabled

## [0.2.1] - 2020-02-28
### Fixed
- Added compatibility with Project service v 0.1.1
- Param values and defaults are strings now
- min, max stored in extra as JSON string

## [0.2.0] - 2020-02-20
### Changed
- ExecuteAction RPC.
- Uuid for action object/point/action.
- Execution proxy PUT method
- ActionPoint class in execution package
- Removed loop in main script, when hasLogic == false
- Parameter values not send in currentAction event
- ProjectState RESUMED removed
- Execution: print out script output if not JSON.
- Joint: rotation -> value


## [0.1.7] - 2019-12-24
### Fixed
- Build: disable caching

## [0.1.5] - 2019-12-22
### Fixed
- Parameter plugins

## [0.1.4] - 2019-12-18
### Fixed
- Parameter of type relative_pose now accepts json string as value

## [0.1.3] - 2019-12-18
### Fixed
- N/A

## [0.1.2] - 2019-12-17
### Fixed
- bump docker version

## [0.1.1] - 2019-12-17
### Fixed
- bump docker version

## [0.1.1] - 2019-12-12
### Fixed
- N/A

## [0.1.0] - 2019-12-12
### Changed
- Separation of services.

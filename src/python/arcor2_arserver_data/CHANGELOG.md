# Changelog

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),

## [0.20.0] - 2022-03-25

### Added

- New RPC definitions `GetScene` and `GetProject`.

## [0.19.0] - 2022-01-25

### Changed

- Breaking change of WebSockets API (`ActionStateBefore` event).
- Switched to Python 3.9, updated dependencies.

## [0.18.0] - 2021-10-25

### Changed

- New RPCs `UpdateObjectModel` and `ObjectTypeUsage`. 
- `ListScenes` and `ListProjects` updated.
- `DeleteObjectType` replaced with `DeleteObjectTypes`.
- `TemporaryPackage` now has (optional) debugging-related args.

## [0.17.0] - 2021-08-05

### Changed

- Flag for linear movement for added to some RPCs.


## [0.16.0] - 2021-07-29

### Changed

- Support for multi arm robots.
  - `arm_id` parameter added into relevant RPCs. 
- Change constants to project parameters.
- Object aiming RPCs updated.
  - RPCs were renamed and all of them now have `dry_run`.
  - There is a new method to cancel the process.

## [0.15.0] - 2021-06-11

### Changed

- Updated to work with Project service 0.8.0.
  - `ProjectConstant` renamed to `ProjectParameter`.

## [0.14.0] - 2021-05-21

### Changed

- Return value of `GetCameraPose` RPC updated.
- Locking-related RPCs and events.
- New RPC `AddApUsingRobot`.

### Fixed
- ObjectType which source code contained Windows line endings was always evaluated as modified.

## [0.13.0] - 2021-03-30

### Changed

- New RPC `SetEefPerpendicularToWorld`.
- New RPC `StepRobotEef`.

## [0.12.0] - 2021-03-03

### Changed
- `CopyActionPoint` RPC added.
- `HandTeachingMode` RPC and event added.
- `safe` added to `MoveToPose`, `MoveToJoints`, `MoveToActionPoint`.

## [0.11.0] - 2021-02-08

### Changed
- `Calibration` RPC renamed to `GetCameraPose`.
- New `MarkersCorners` RPC.

## [0.10.0] - 2020-12-14

### Changed
- `ActionResult` event changed to match with `ActionState` (support for actions that may return more than one result).
- `ProcessState` event for signalling state of long-running processes.
- RPCs for camera/robot calibration.

### Changed
- RPC for IK/FK.

## [0.9.2] - 2020-10-30

### Changed
- RPC for IK/FK.


## [0.9.1] - 2020-10-19

### Changed
- ARCOR2 dependency updated

## [0.9.0] - 2020-10-16

### Changed
- WS API for updates of scene objects parameters and management of project-defined overrides.
- `UpdateObjectPose` and `UpdateActionPointPosition` now has dry_run.
- Box/Cylinder/Sphere models now have some constraints on their dimensions (checked in `__post_init__`).

## [0.8.0] - 2020-09-24
### Changed
- The first release of the separated package.

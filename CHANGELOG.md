# Changelog
Major version bumps should be reserved for API-breaking releases or significant changes in functionality. Minor versions should be used for all other bug fixes and new options.

## Legend
- *ADDED*: New feature usually optional and non-breaking
- *REMOVED*: Functionality removed, reserved for major version bumps
- *BUGFIX*: Regression fixed, usually with additional test coverage
- *CHANGE*: Behavior change of existing functionality, reserved for major version bumps

## Versions
### 1.0.8
- *ADDED* Added the vobject library (stripping it down to just the vcard class).

### 1.0.7
- *BUGFIX* Fix the correct encoding in py2 and py3 for unicode characters outside the BMP

### 1.0.6
- *BUGFIX* Fix `total_segment_length` calculation for UCS-2 encoding
- *BUGFIX* Calculate MMS properties similar to how UCS-2 encoding is calculated

### 1.0.5
- *ADDED* Add a "max_segment_size" field in the profile response.
- *BUGFIX* Fix the "message" in the segment body

### 1.0.2 (Mar 31, 2020)
- *BUGFIX*: Better handling of utf-8 encoded strings.
### 1.0.1 (Feb 5, 2020)
- *ADDED*: Add support for message normalization.
- *ADDED*: Add this changelog.
### 1.0 (Dec 2, 2019)
- Initial release.

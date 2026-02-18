# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Comprehensive README.md with detailed project documentation
- Step-by-step Pixabay API key tutorial with multiple methods
- Application screenshots embedded in README
- Project structure diagram in documentation
- Troubleshooting table with common issues and solutions
- Security & Privacy section explaining local data storage
- Roadmap and future enhancement plans
- Contributing guidelines
- Tips for best user experience

### Changed
- Updated app data storage path to `C:\Users\[username]\AppData\Roaming\DarshilSoft\Pixelverse\`
- Renamed internal file references from `cat.csv` to `profile.csv` for smart category management
- Improved README documentation with professional formatting and emoji icons
- Enhanced project description with key features and benefits
- Updated configuration documentation to reflect new file structure

### Fixed
- Fixed missing comma in category query list (`windows wallpaper` and `amoled dark wallpaper`)
- Fixed pandas DataFrame CSV export creating unnamed index column by adding `index=False` parameter in `category.py`
- Added proper return statement for first-time CSV initialization in `get_category()` function

### Improved
- Better documentation of wallpaper temporary storage (`temp.jpg`)
- Clearer explanation of smart category scoring system in `profile.csv`
- More detailed storage location documentation with full paths
- Enhanced user guidance for getting started with the application

## Notes

- `profile.csv` now properly tracks category usage without generating unnamed columns
- `temp.jpg` stores wallpaper images locally until they are applied to the desktop
- App data path follows Windows convention using DarshilSoft namespace

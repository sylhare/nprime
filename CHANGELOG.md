# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.3.0]

### Added
- CONTRIBUTING.md with comprehensive development setup and deployment instructions
- CHANGELOG.md for tracking project changes and releases

### Changed
- Modernized Python code notation for better performance and readability:
  - Replaced `pow(n, 0.5)` with `math.isqrt(n)` for integer square root operations
  - Updated string formatting from `.format()` to f-strings throughout test suite
  - Improved type checking using `isinstance()` with proper bool handling
- Enhanced development workflow documentation

### Removed
- Obsolete `# -*- coding: utf-8 -*-` declarations from all Python files

## [1.2.1] - Latest Release

### Added
- Postponed Sieve of Eratosthenes algorithm for efficient prime generation
- Support for generating primes starting from a specific number
- Comprehensive test coverage with multiple prime testing algorithms
- Modern Python packaging with pyproject.toml configuration
- Enhanced visualization functions for prime number patterns

### Fixed
- Bug fixes and stability improvements

## [1.2.0] - Previous Release

### Added
- Miller-Rabin primality test implementation
- Fermat primality test for probabilistic prime checking
- Trial division algorithm for educational purposes
- Comprehensive test suite for all algorithms

### Changed
- Performance improvements and code refactoring

## [1.1.0] - Previous Release

### Added
- Sieve of Eratosthenes implementation
- Basic prime generation functions
- Initial test suite and validation
- Performance optimizations

### Changed
- Algorithm optimizations and improvements

## [1.0.0] - Initial Release

### Added
- Basic `is_prime()` function for primality testing
- `generate_primes()` function for creating lists of primes
- `find_primes()` function for finding primes in ranges
- Core mathematical algorithms for prime number operations
- Basic visualization capabilities
- Initial documentation and examples
- Cross-platform compatibility
- Comprehensive error handling

### Features
- Support for various prime testing algorithms
- Efficient prime generation up to specified limits
- Mathematical visualization tools
- Modular design for extensibility
- Educational and research-focused implementations

---

## Release Notes

### Version Numbering
This project follows [Semantic Versioning](https://semver.org/):
- **MAJOR** version for incompatible API changes
- **MINOR** version for backwards-compatible functionality additions  
- **PATCH** version for backwards-compatible bug fixes

### Change Categories
- **Added** for new features
- **Changed** for changes in existing functionality
- **Deprecated** for soon-to-be removed features
- **Removed** for now removed features
- **Fixed** for any bug fixes
- **Security** for vulnerability fixes

### Development Workflow
For contributors releasing new versions:
1. Update version in `nprime/__init__.py`
2. Move unreleased changes to new version section
3. Update comparison links
4. Create git tag and push

### Links
- [Unreleased]: https://github.com/Sylhare/nprime/compare/v1.2.1...HEAD
- [1.2.1]: https://github.com/Sylhare/nprime/compare/v1.2.0...v1.2.1
- [1.2.0]: https://github.com/Sylhare/nprime/compare/v1.1.0...v1.2.0
- [1.1.0]: https://github.com/Sylhare/nprime/compare/v1.0.0...v1.1.0
- [1.0.0]: https://github.com/Sylhare/nprime/releases/tag/v1.0.0 
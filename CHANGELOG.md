# Changes

## 2.3.0

### Application Changes

- Add support for displaying panelist decimal scores stored in a new table column in the Wait Wait Stats Database instead of the standard integer scores. This is handled via version 2.2.0 of the `wwdtm` library and a new `use_decimal_scores` setting in the `config.json` application configuration file. By default, the value will be set to `false` and must be changed to `true`, and the appropriate changes have been deployed to the Wait Wait Stats Database.
- Increase digits after the decimal point in the "Monthly Average Score Heatmap" from 4 to 5 for consistency
- Removed Aggregate Count plot from the "Panelist: Score Breakdown" chart
- Add a new `use_latest_plotly` setting in the `config.json` application configuration file to set whether or not to use the stable version symlinked as `plotly-stable.min.js` or the latest version symlinked as `plotly-latest.min.js`. For backward compatibility, `plotly.min.js` is a symlink that points to `plotly-stable.min.js`

### Component Changes

- Upgrade wwdtm from 2.1.0 to 2.2.0, which also includes the following changes:
  - Upgrade NumPy from 1.24.2 to 1.24.3
- Upgrade Plotly.js from 2.23.1 to 2.25.2 (stable) and 2.26.0 (latest)

### Development Changes

- Upgrade black from 23.3.0 to 23.7.0

## 2.2.6

### Component Changes

- Upgrade Plotly.js from 2.20.0 to 2.23.1

## 2.2.5

### Component Changes

- Upgrade Flask from 2.2.3 to 2.3.2
- Upgrade wwdtm from 2.0.8 to 2.1.0, which also includes the following changes:
  - Upgrade MySQL Connector/Python from 8.0.31 to 8.0.33
  - Upgrade NumPy from 1.23.4 to 1.24.2
  - Upgrade python-slugify from 6.1.2 to 8.0.1
  - Upgrade pytz from 2022.6 to 2023.3

### Development Changes

- Move pytest configuration from `pytest.ini` into `pyproject.toml`
- Upgrade flake8 from 5.0.4 to 6.0.0
- Upgrade pycodestyle from 2.9.1 to 2.10.0
- Upgrade pytest from 7.2.0 to 7.3.1
- Upgrade black from 22.10.0 to 23.3.0

## 2.2.4

### Component Changes

- Upgrade Materialize from 1.2.1 to 1.2.2
- Upgrade Plotly.js from 2.18.1 to 2.20.0

## 2.2.3

### Component Changes

- Upgrade Flask from 2.2.2 to 2.2.3
- Upgrade Werkzeug from 2.2.2 to 2.2.3 to fix a security vulnerability

## 2.2.2

### Component Changes

- Upgrade Plotly.js from 2.17.0 to 2.18.1

## 2.2.1

### Application Changes

- Fix issue with `stats_url` not being added to `app.jinja_env.globals` upon application startup

## 2.2.0

### Component Changes

- Upgrade Materialize from 1.1.0 to 1.2.1

### Application Changes

- Restructuring template folder locations to match the structure used by the [Wait Wait Stats Page](https://github.com/questionlp/stats.wwdt.me_v5) and [Wait Wait Reports](https://github.com/questionlp/reports.wwdt.me_v2)

### Other Changes

- Updating copyright year for all code files and add copyright block to `static/css/style.css` and `static/js/init.js`

## 2.1.7

### Component Changes

- Upgrade Plotly.js from 2.13.3 to 2.17.0

## 2.1.6

### Application Changes

- Use `dict.get(key, default_value)` in `app/__init__.py` to get/set configuration values in order to avoid application startup errors if configuration keys are not set
  - Default value for `time_zone` is `UTC`
  - Default values for any URL is an empty string
- Adding `mastodon_url` and `mastodon_user` configuration keys in the `settings` section of the config file
- If the `mastodon_url` and `mastodon_user` keys contain a value, insert a link with `rel="me"` attribute for profile link validation, in the page footer

### Component Changes

- Upgrade wwdtm from 2.0.7 to 2.0.8, which also includes the following changes:
  - Upgrade MySQL Connector/Python from 8.0.30 to 8.0.31
  - Upgrade NumPy from 1.23.2 to 1.23.4
  - Upgrade python-slugify from 5.0.2 to 6.1.2
  - Upgrade pytz from 2022.2.1 to 2022.6
- Upgrade Flask from 2.2.0 to 2.2.2
- Upgrade Werkzeug from 2.2.1 to 2.2.2

### Development Changes

- Upgrade flake8 from 4.0.1 to 5.0.4
- Upgrade pycodestyle from 2.8.0 to 2.9.1
- Upgrade pytest from 7.1.2 to 7.2.0
- Upgrade black from 22.6.0 to 22.10.0

## 2.1.5

### Bugfix

- Fix an issue where the `time_zone` configuration value was being assigned to `settings_config` twice, instead of being assigned to both `settings_config` and `database_config`

## 2.1.4

### Bugfix

- Fix an issue where an incorrect route was being referenced in `panelists.routes.score_breakdown_details()`, causing an unhandled error

## 2.1.3

### Component Changes

- Upgrade wwdtm from 2.0.5 to 2.0.7, which also includes the following changes:
  - Upgrade MySQL Connector/Python from 8.0.28 to 8.0.30
  - Upgrade NumPy from 1.22.3 to 1.23.2
  - Upgrade pytz from 2022.1 to 2022.2.1

### Application Changes

- Add an additional query that unsets `ONLY_FULL_GROUP_BY` flag and sets the appropriate flags for the session-level `sql_mode` for queries that return an error due to MySQL Server setting the `ONLY_FULL_GROUP_BY` flag by default. Queries and application logic for the respective functions will need to be rearchitected in a future release.

## 2.1.2

### Component Changes

- Upgrade Plotly.js from 2.12.1 to 2.13.3

## 2.1.1

### Application Change

- Made changes to how gender is referenced in the dataset names for the Panel Gender Mix chart and update the corresponding test

## 2.1.0

### Component Changes

- Upgrade Flask to 2.2.0
- Upgrade Werkzeug from 2.1.2 to 2.2.1
- Upgrade Plotly.js from 2.11.1 to 2.12.1

### Application Changes

- Update guests, hosts, locations, panelists, scorekeepers and shows routes and redirects so that canonical routes now have a trailing slash and requests made without a trailing slash will get redirected

### Development Changes

- Upgrade pytest from 6.2.5 to 7.1.2
- Add type hinting to pytest scripts
- Upgrade Black from 22.1.0 to 22.6.0
- Change Black `target-version` to remove `py36` and `py37`, and add `py310`

## 2.0.1

### Application Changes

- Fixed typo in `500` error page

## 2.0.0

### Component Changes

- Replace (lib)wwdtm 1.2.x with wwdtm 2.0.5 (or higher)
- Upgrade Flask from 2.0.1 to 2.1.1
- Upgrade Materialize from 1.0.0 to 1.1.0
- Upgrade Plotly.js from 2.4.2 to 2.11.1

### Application Changes

- Complete restructuring of the Flask application to use Blueprints design
pattern
- Convert the application from using uWSGI to serve the application to
  Gunicorn to match the changes made with the Wait Wait Stats API and Wait
  Wait Stats Page

### Development Changes

- Adding tests by way of `pytest`
- Introduction of `black` for code formatting

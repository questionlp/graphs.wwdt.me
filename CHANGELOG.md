# Changes

## 3.4.4

### Component Changes

- Upgrade wwdtm from 2.18.2 to 2.19.0
- Upgrade wwdtm-theme from 2.0.5 to 2.0.20, which includes:
  - Upgrade Bootstrap from 5.3.6 to 5.3.7

## 3.4.3

### Application Changes

- Update list of AI scraper user agents
- Change the `block_ai_scrapers` logic so that if the configuration key is set to `true`, the action is set to `Disallow: /`. If the configuration key is set to `false`, the action is set to `Crawl-delay: 10`

## 3.4.2

### Component Changes

- Upgrade Flask from 3.1.0 to 3.1.1

## 3.4.1

### Application Changes

- Set external links (including Wait Wait Graphs, Wait Wait Reports and Wait Wait Stats API) to open in a new window/tab
- Add `bluesky_url` and `bluesky_user` configuration to display Bluesky account information
- Add Bluesky link in footer if the above configuration keys have been set

### Component Changes

- Upgrade wwdtm from 2.18.1 to 2.18.2
- Upgrade wwdtm-theme from 2.0.0 to 2.0.5
  - Upgrade Bootstrap from 5.3.5 to 5.3.6
  - Upgrade Bootstrap Icons from 1.11.3 to 1.13.1

### Development Changes

- Upgrade ruff from 0.9.6 to 0.11.9
- Upgrade pytest from 8.3.3 to 8.3.5
- Upgrade pytest-cov from 5.0.0 to 6.1.1

## 3.4.0

Due to the significant changes around the new application theming, the usual Application, Component and Development changes section are being merged into a single Changes section.

### Changes

- Complete re-work of the application theme structure and how theme assets are deployed
  - `scss` submodule has been replaced by `wwdtm-theme`
  - `wwdtm-theme` now handles the compiling of the Sass files to CSS into `dist/css` and copies the Bootstrap scripts into `dist/js`
- Trimming down the included `package.json` to only require `@ibm/plex-mono` and `@ibm/plex-sans`
- NPM scripts have been simplified to copy the required CSS and JS files from `wwdtm-theme` and the required IBM Plex web font files into the appropriate paths under `app/static`
- Upgrade wwdtm from 2.17.2 to 2.18.1
- Upgrade Plotly.js v3 from 3.0.0 to 3.0.1

## 3.3.5

### Application Changes

- Relocate the Bootstrap and application code initialization from towards the end of the document to the head to prevent background flashing on page loads when in dark mode
- Corrected Umami Analytics include for error page template
- Update Bootstrap icon classes to include `.bi`

### Component Changes

- Set Jinja2 version to `~=3.1.6`

## 3.3.4

### Application Changes

- Update list of AI bots from <https://github.com/ai-robots-txt/ai.robots.txt> in the default `robots.txt`

### Component Upgrades

- Upgrade wwdtm from 2.14.0 to 2.17.2

### Development Changes

- Upgrade ruff from 0.9.2 to 0.9.6
- Remove black from required development packages as part of migrating entirely to Ruff

## 3.3.3 (Not Released)

### Component Changes

- Upgrade Plotly.js v3 from 3.0.0-rc.2 to 3.0.0

### Development Changes

- Upgrade ruff from 0.7.4 to 0.9.2
- Ran `ruff format` to format Python code files using the Ruff 2025 Style Guide

## 3.3.2

### Component Changes

- Upgrade Flask from 3.0.3 to 3.1.0

## 3.3.1

### Component Changes

- Upgrade Plotly.js v2 from 2.35.2 to 2.35.3
- Upgrade Plotly.js v3 from 3.0.0-rc.1 to 3.0.0-rc.2
- Upgrade nanoid from 3.3.7 to 3.3.8 to fix a security vulnerability for a package required to compile, minify and copy generated CSS files

## 3.3.0

### Application Changes

- Replace the `use_latest_plotly` application configuration setting with `use_plotly_v3` to set the version of Plotly.js to use in the application. The default value is `false`.
- Remove the `stable` and `latest` labels from Plotly.js versions. See "Component Changes" for more information.
- Change the color scale for both "Monthly Aggregate Score" and "Monthly Average Score" heatmaps to provide more contrast across the range.
  - Use different color scales for "Monthly Aggregate Score" and "Monthly Average Score" heatmaps due to the former having an order of magnitude large scale.
- Standardize on colors from the [IBM Design Language](https://www.ibm.com/design/language/color/) for chart colorways.
- Add missing page titles on various pages.
- Standardize use of `page_title` variable across all Panelists and Shows pages.

### Component Changes

- Upgrade Plotly.js versions and introduce Plotly.js 3.0.0-rc.1
  - Plotly.js v2.x has been upgraded from 2.28.0 (formerly labeled `stable`) and 2.35.0 (formerly labeled `latest`) to 2.35.2
    - Both `plotly-latest.min.js` and `plotly-stable.min.js` symlinks will point to `plotly.min.js`, which in turn points to 2.35.2
  - Setting `use_plotly_v3` to `true` will use 3.0.0-rc.1
  - Previous versions of the Plotly.js files remain under `app/static/js` for the time being and will be removed in a future release

## 3.2.2

### Application Changes

- Update `wwdtm-theme` to set font weight for header and footer navigation links to `500`
- Tweak responsive font sizing for `root` in `wwdtm-theme` with a range of 14.5px and 16.75px

## 3.2.1

### Application Changes

- Re-add responsive font sizing for `:root` in `wwdtm-theme` with a range of 14px and 16.5px

## 3.2.0

### Application Changes

- Remove responsive font sizing for `:root` in `wwdtm-theme`.

### Component Changes

- Upgrade wwdtm from 2.12.1.post0 to 2.14.0

### Development Changes

- Upgrade ruff from 0.6.9 to 0.7.4
- Upgrade black from 24.8.0 to 24.10.0

## 3.1.0

### Application Changes

- Replace all references of `named_tuple=` in database cursors to `dictionary=` due to cursors using `NamedTuple` being marked for deprecation in future versions of MySQL Connector/Python
- Update code that is impacted by the database cursor type change from `NamedTuple` to `dict`

### Component Changes

- Upgrade wwdtm from 2.11.0 to 2.12.1.post0

### Development Changes

- Add initial pytest coverage reporting using `pytest-cov`, which can be generated by running: `pytest --cov=app tests/`
- Correct naming of testing function for `robots.txt` route

## 3.0.2

### Application Notes

- Add missing Umami Analytics config logic update

## 3.0.1

### Application Notes

- Add missing Umami Analytics template file

## 3.0.0-post0

### Application Changes

- This non-release does not include any application changes. The version number presented by the application will still be [3.0.0](https://github.com/questionlp/graphs.wwdt.me/releases/tag/v3.0.0).

### Development Changes

- Removal of the `serve` NPM package as it is not used and one of its dependencies requires a package that has a [high severity vulnerability](https://github.com/advisories/GHSA-9wv6-86v2-598j).

## 3.0.0

### Application Changes

- Frontend code refactor due to switching from Materialize to Bootstrap
  - Replacing Materialize frontend toolkit with Bootstrap
  - Replacing Materialize Icons with Bootstrap Icons
  - Refactor the frontend structure to use Bootstrap frontend components and conventions
  - Include the required IBM Plex web fonts with the application to remove use of Google Fonts
- User interface changes
  - Change the behavior of the main navigation to combine navigation links into a single list that are listed in the top navbar on `xl` screen size or in an off-canvas side nav on smaller screens
  - Improve legibility and readability in font size changes and increased color contrast when using the dark mode color theme
  - Include a color theme toggle in the main navigation to allow the reader to switch the theme on-the-fly
    - **Note**: When switching color themes on a page that contains a chart, you will need to reload the page in order to render the chart in a matching color theme.
- Fix warnings and errors reported by pylint
- Add an experimental `block_ai_scrapers` config key that will block known AI scraping and crawling bots (default: false)
- Cleanup configuration processing code

### Component Changes

- Upgrade gunicorn from 22.0.0 to 23.0.0
- Replace Materialize CSS 1.2.2 with Bootstrap 5.3.3
  - Existing Materialize CSS and JS files will be preserved to prevent cached versions of the application from breaking
  - Materialize-related files will be removed in a future minor release
- Upgrade Plotly.js from 2.25.2 to 2.28.0 (stable) and from 2.28.0 to 2.35.0 (latest)

## 2.10.1

### Application Changes

- Move web analytics tags out of `base.html` into `head.html`

## 2.10.0

### Application Changes

- Add support for Umami web analytics via `settings.umami_analytics` config object with the following keys:

| Config Key | Description |
| ---------- | ----------- |
| `_enabled` | Set value to `true` to enable adding Umami `script` tag (default: `false`) |
| `url` | URL of the Umami analytics script |
| `data_website_id` | Umami Site ID |
| `data_auto_track` | Set value to `false` to disable auto event tracking (default: `true`) |
| `data_host_url` | Override the location where Umami data is sent to |
| `data_domains` | Comma-delimited list of domains where the Umami script should be active |

## 2.9.0

### Application Changes

- Change the database queries and application logic for several modules to remove the need to unset the MySQL session variable `ONLY_FULL_GROUP_BY`
- Add experimental support for MariaDB 11.4.2

### Development Changes

- Upgrade ruff from 0.3.6 to 0.5.1
- Upgrade black from 24.3.0 to 24.4.2
- Upgrade pytest from 8.1.1 to 8.1.2

## 2.8.5

### Application Changes

- Change the footer font color to remove alpha transparency to improve readability

## 2.8.4

### Component Changes

- Upgrade wwdtm from 2.8.2 to 2.10.0, which requires Wait Wait Stats Database version 4.7 or higher

## 2.8.3

### Component Changes

- Upgrade wwdtm from 2.8.0 to 2.8.2
- Upgrade flask from 3.0.0 to 3.0.3
- Upgrade gunicorn from 21.2.0 to 22.0.0

### Development Changes

- Upgrade ruff from 0.1.13 to 0.3.6
- Upgrade pytest from 7.4.4 to 8.1.1

## 2.8.2

### Development Changes

- Upgrade black from 23.12.1 to 24.3.0

## 2.8.1

### Application Changes

- Add support for GitHub sponsorship link in the side pop-out nav, dropdown nav menu and in the footer by way of the `settings.github_sponsor_url` config key
- Change link color to match that of the Wait Wait Stats Page link color
- Change the how render and version information is rendered on screens with a width less than 1200px to align left rather than right

## 2.8.0

### Application Changes

- General code cleanup and fixing typos
- Add support for Patreon link in the side pop-out nav, dropdown nav menu and in the footer by way of the `settings.patreon_url` config key
- Upgrade Plotly.js latest version from 2.26.0 to 2.28.0
- Calculate the appropriate value for the max y-axis range for the Bluff the Listeners Counts chart

### Component Changes

- Upgrade wwdtm from 2.6.1 to 2.8.0

### Development Changes

- Switch to Ruff for code linting and formatting (with the help of Black)
- Upgrade black from 23.11.0 to 23.12.1

## 2.7.1

### Component Changes

- Upgrade wwdtm from 2.6.0 to 2.6.1

## 2.7.0

### Component Changes

- Upgrade wwdtm from 2.5.0 to 2.6.0, which requires Wait Wait Stats Database version 4.4 or higher

## 2.6.1

### Application Changes

- Remove unneeded slash in an empty tag for the Materialize CSS include

## 2.6.0

**Starting with version 2.6.0, support for all versions of Python prior to 3.10 have been deprecated.**

### Application Changes

- Replace `dateutil.parser.parse` with `datetime.datetime.strptime`

### Component Changes

- Upgrade wwdtm from 2.4.1 to 2.5.0, which drops supports for Python versions prior to 3.10 and includes:
  - Upgrade MySQL Connector/Python from 8.0.33 to 8.2.0
  - Upgrade numpy from 1.24.4 to 1.26.0

### Development Changes

- Upgrade black from 23.10.1 to 23.11.0
- Remove `py38` and `py39` from `tool.black` in `pyproject.toml`
- Bump minimum pytest version from 7.0 to 7.4 in `pyproject.toml`

## 2.5.0

### Component Changes

- Upgrade Flask from 2.3.2 to 3.0.0
- Upgrade gunicorn from 20.1.0 to 21.2.0

### Development Changes

- Upgrade pycodestyle from 2.11.0 to 2.11.1
- Upgrade pytest from 7.4.0 to 7.4.3
- Upgrade black from 23.7.0 to 23.10.1

## 2.4.0

### Component Changes

- Upgrade wwdtm from 2.2.0 to 2.4.0

## 2.3.1

### Application Changes

- Fix a bug with Panelists: Scores by Appearance route where panelists who have appearances on the show, but do not have corresponding scores, causes an error.

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
- Upgrade flake8 from 6.0.0 to 6.1.0
- Upgrade pycodestyle from 2.10.0 to 2.11.0
- Upgrade pytest from 7.3.1 to 7.4.0

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

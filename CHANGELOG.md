# Changes

## 2.1.1

- Made changes to how gender is referenced in the dataset names for the Panel Gender Mix chart and update the corresponding test

## 2.1.0

### Component Changes

- Upgrade Flask to 2.2.0
- Upgrade Werkzeug from 2.1.2 to 2.2.1
- Upgrade Plotly JS from 2.11.1 to 2.12.1

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
- Upgrade Plotly JS from 2.4.2 to 2.11.1

### Application Changes

- Complete restructuring of the Flask application to use Blueprints design
pattern
- Convert the application from using uWSGI to serve the application to
  Gunicorn to match the changes made with the Wait Wait Stats API and Wait
  Wait Stats Page

### Development Changes

- Adding tests by way of `pytest`
- Introduction of `black` for code formatting

# Authorization: public paths (`EXCLUDE_PATHS`)

The module `app/config/authorization.py` defines **`EXCLUDE_PATHS`**: URL paths that **do not** require a valid JWT. The [`AuthorizationMiddleware`](../app/middleware/authorization_middleware.py) skips bearer-token verification when the incoming request path matches any entry.

Everything else expects an `Authorization: Bearer <token>` header (unless you add another layer of auth elsewhere).

## Editing the config

Only change the `EXCLUDE_PATHS` list in `app/config/authorization.py`. Add or remove string entries as needed. Path matching rules are implemented in [`app/lib/auth_path_utils.py`](../app/lib/auth_path_utils.py).

## How matching works

Request paths are normalized (trailing slashes stripped; the site root `/` is treated as a special case). Each pattern in `EXCLUDE_PATHS` can be:

| Kind | Example | Matches |
|------|---------|---------|
| **Exact** | `/api/v1/users/login` | Only that path (with or without a trailing slash). |
| **Prefix** | `/api/v1/news/*` | The prefix path and any subpath (e.g. `/api/v1/news`, `/api/v1/news/latest`). Does not match a different prefix such as `/api/v1/newsletter`. |
| **Segment wildcard** | `/api/v1/product/*/delete` | Each `*` is exactly one path segment, e.g. `/api/v1/product/42/delete`. |

Invalid pattern: `/*` alone (raises at startup). Use `/` for the root URL.

## Flow

1. `app/config/authorization.py` exports `EXCLUDE_PATHS`.
2. `app/middleware/authorization_middleware.py` builds a checker once: `excluded_path_checker(EXCLUDE_PATHS)` from `auth_path_utils`.
3. If the path is excluded, the request proceeds without JWT validation; otherwise the middleware validates the token and attaches user data to `request.state`.

## Security notes

- Prefer **narrow** entries (exact paths) for anything sensitive.
- Prefix patterns (`.../*`) make **every** route under that prefix public; use only when that is intentional.
- After changing `EXCLUDE_PATHS`, smoke-test login vs protected routes so you do not accidentally expose APIs.

## Related tests

Unit tests for path rules live in `app/tests/unit/test_auth_path_utils.py`.

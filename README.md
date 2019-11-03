# Introduction

SCA is a small API that was conjured together to managed users and public SSH keys, and was designed to use Automata to create user accounts on systems Automata is installed on.

# Installation

The easiest way is to just grab the Docker image (`jamesthebard/sca:latest`), configure it, and then let it do work.

Unfortunately, the app currently does require that you add people, groups, and SSH keys via API calls, but development is in the works to add some CLI utilities to make things a lot easier.

# Configuration

There are some environment variables that need to be set:

- `APP_DEFAULT_USERNAME|admin`: The username of the administrator.
- `APP_DEFAULT_PASSWORD|password`: The default password.
- `APP_DEFAULT_ADMIN_GROUP|sca_admin`: The default group name.  Members in this group will be able to add users/groups/etc. to anyone in SCA.  Do not put non-administrators in this group.
- `DATABASE_URL|sqlite:///app.db`: The connection to the database.  It will, however, support any DB connection that SQLAlchemy does.

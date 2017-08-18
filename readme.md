# Organization Project

Aim is to be able to create users under specific organizations
Said users will be able to create and add links under those organizations
Said users will only be able to view links of those organizations everytime they login
Users will also be able to edit and delete those links.

#### Major Libraries used:
1. Rest-auth library for implementing user registration and login
2. Swagger for making a good looking documentation
3. JWT for generating tokens upon login. Both session and token based logins
are enabled
4. Factory boy for generating models for easier implementation of unit tests.


#### Tweaks and Modifications:
1. Implemented a signal that made makes user a staff upon registration (creation of a user object that is).
2. An extra permission class called "OrganizationPermission" which raises a validation error (clean error handling) if a user that is registered is not part of an organization.
3. Implemented unit tests to add, modify and delete iframe links.

#### Super admin credentials for the existing database:
username = admin
password = admin

(P.S: Please login using username and password when navigating the django rest framework.)

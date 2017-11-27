=================
GitHub replicator
=================

What is this ?
==============

This is a tool that can be used for selective replication of git repositories
to GitHub organizations, for groups not using GitHub as their main development
toolkit but still wanting to publish code to GitHub as a marketing property.

How does this work ?
====================

Triggers trigger replication actions (for example, watching a MQTT event
stream for change-merged events emitted by Gerrit).

Mappers map local repository names to GitHub repository names.

ghreplicator then fetches the new refs from the local repository and push
them to the repository in the mapped organization.

Testing
=======

* Copy config.json.sample to config.json and edit configuration.
* Run tox -e venv -- ghreplicator -d config.json

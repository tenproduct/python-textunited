=====
Usage
=====

To use python-textunited in a project::

	import textunited



Authenticate
------------

This example show how to get the client. This client will be used on the
examples below

.. code:: python

    from textunited import TextUnitedClient

    client = TextUnitedClient(company_id='123', api_key='abc')

List all account
----------------

.. code:: python

    account_list = client.list_accounts()

    for account in account_list:
        print(account)

    # it will show something similar:
    # id#001 user001@example.com
    # id#002 user002@example.com
    # id#003 user003@example.com

List all projects and get files content
---------------------------------------

In this example, it is showed how to list projects and access to the to
the file content. For more info, please check the documentation inside
of each model.

.. code:: python

    projects_list = client.list_projects()

    for project in projects_list:
        print(project)

    # it will show something similar to:
    # id#0001 "example1" EN -> AR by Jonh Example (Completed)
    # id#0002 "example2" EN -> AR by Jonh Example (In preparation)


    # Get files inside project. Content is not downloaded, only the metadata
    file_list = projects_list[0].get_files()
    file = file_list[0]

    # if the status is Translated, we can get translated files
    file.get_translated_content()
    file.translated_content

    # Also, it is possible to download the source content
    file.get_source_content()
    file.source_content

Create a new project
--------------------

A project is composed by multiple files to be translated, each file
needs to be encapsulated in a FileUpload class and pass in a list to
Project Request.

.. code:: python

    from textunited import FileUpload, ProjectRequest

    file1 = FileUpload(name='example1.txt', b'hello world')
    file2 = FileUpload(name='example1.txt', b'hello world')

    project_request = ProjectRequest(
        name='Project 1',
        source_language_id=12,
        target_language_id=13,
        description='This is a description',
        files=[file1, file2],
        translator_id=12,
    )

    project_id = client.add_project(project_request)

    client.get_project(project_id)

# PWN Guide
1. Files to upload to ctf, place them into ``\Uploads`` folder.
2. Writeup for the task can be placed into ``\Writeup`` folder.
3. File for the challenge itself to be hosted need to be placed into ``\Challenge``
    - source for creating the challenge need to be places in ``\Challenge\src``
3. Edit challange.yml so that it contains the following
    - name of the task
    - description of the task, you can also add in author for the task here.
    - category
    - flags
    - files
        - this should contain the path of the file/files you placed into the ``\Uploads`` folder.
    - connection_string
        - where and how will they perform their exploit (ex. connection_string: nc chall_name.chall.tghack.no, connection_string: https://chall_name.chall.tghack.no)
4. After you have followed each of the steps, delete this file, as a sign that this task is ready.

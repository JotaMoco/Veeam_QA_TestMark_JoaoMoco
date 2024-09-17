Veeam QA Test Mark created by João Moço
Before using the synchronization tool:
-> The folder 'test1' is a test source folder with 2 .txt files;
-> (Optional) For testing purposes, create an empty folder; 
Using the synchronization tool:
-> Open the Command Prompt or the Terminal in Visual Studio Code (VSC);
-> Write 'cd (path where folder with 'sync_test.py' file is located)' and execute;
-> There are 2 required and 2 optional arguments:
---> '--source'(required): source folder path;
---> '--replica'(required): source folder path;
---> '--interval'(optional): Interval of time between synchronization cycles in seconds. Default time is 60 seconds;
---> '--cycles'(optional): Amount of synchronization cycles. Default value is 1 cycle;
-> Write 'python sync_test.py -- source SOURCE --replica REPLICA [--interval INTERVAL] [--cycles CYCLES]' and execute;
-> Log file 'log_(current day)_(current time).txt' will be created in the same folder where the work is being done and shown in the CLI;

For any questions, contact:
-> Email: joaofmoco@gmail.com
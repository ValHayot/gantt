# Gantt

A simple script to draw a Gantt chart from a computing trace.

Tasks must be written in a JSON file with the following syntax:
```
{
    "tasks": [
       {
            "name": "task1",
            "id": 0,
            "start-time": 0,
            "end-time": 10,
            "node": "node1"
        },
        {
            "name": "task2",
            "id": 1,
            "start-time": 10,
            "end-time": 20,
            "node": "node1"
        }
}
```

See example in `tasks.json`.

Usage: `gantt.py tasks.json gantt.pdf`.

Example: 

![Example of Gantt chart](https://raw.githubusercontent.com/glatard/gantt/master/gantt.png)

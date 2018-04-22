#!/usr/bin/env python

from random import random
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import json
import argparse


def main():
    parser = argparse.ArgumentParser("Prints a Gantt chart for computing tasks")
    parser.add_argument("tasks_json", action="store",
                    help="JSON file containing task definitions.")
    parser.add_argument("output_file", action="store",
                    help="Output file where to store the results. File type determined from extension.")
    results = parser.parse_args()

    json_string = json.loads(open(results.tasks_json).read())
    assert(json_string.get('tasks')), "Tasks not found in JSON file."
    tasks_json = json_string['tasks']

    node_index = {}
    max_end_time = 0
    for task in tasks_json:
        if task['end-time'] == task['start-time']:
            task['end-time'] += 10**-6  # tasks of length 0 are not possible
        assert(task['end-time'] > task['start-time'])
        if task['end-time'] > max_end_time:
            max_end_time = task['end-time']
        if node_index.get(task['node']) is None:
            node_index[task['node']] = len(node_index)
    n_nodes = len(node_index)

    # Determine max number of concurrent tasks in nodes
    overlaps = {}
    for t in tasks_json:
        overlaps[t['id']] = []
        for u in tasks_json:
            if not (t['node'] != u['node'] or t['end-time'] <= u['start-time'] or u['end-time'] <= t['start-time']):
                overlaps[t['id']].append(u)
        overlaps[t['id']].sort(key=lambda x: x['id'])
        assert(len(overlaps[t['id']]) >= 1)

    # Plot figure
    fig = plt.figure()
    ax1 = fig.add_subplot(111, aspect='equal')

    # Axes
    ax1.set_xlabel("time")
    ax1.get_yaxis().set_visible(False)
    ax1.axes.xaxis.set_ticklabels([0, "", "", "", "", round(max_end_time)])
    for node in node_index.keys():
        ax1.text(-0.2, 1.0/n_nodes*node_index[node]+0.5/n_nodes, node)

    # Tasks
    for task in tasks_json:
        task_duration = task['end-time']-task['start-time']
        height = 1.0/(n_nodes*len(overlaps[task['id']]))
        width = task_duration/float(max_end_time)
        x = task['start-time']/float(max_end_time)
        y = 1.0/n_nodes*node_index[task['node']] + overlaps[task['id']].index(task)*height
        ax1.add_patch(patches.Rectangle(
            (x, y),  # (x,y)
            width,  # width
            height,  # height
            facecolor = (random(), random(), random())
        ))
        if task_duration/float(max_end_time) > 0.1: # add names of tasks that represent more than 10% of the makespan
            ax1.text(x, y+0.5*height, task['id'])

    fig.savefig(results.output_file)

if __name__ == '__main__':
    main()

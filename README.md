# Designing-a-Scheduler-CS110-Assignment


| ID | Description                | Duration | Dependencies               | Status | Type          | Start Time | Academic & Career Importance | Personal Interest |
|----|----------------------------|----------|----------------------------|--------|---------------|------------|---------------------|-------------------|
| 1  | Reading books              | 1.0      | None                       | N       | Regular       | None       | 2                   | 4                 |
| 2  | CS110 PCW                  | 2.0      | None                       | N       | Regular       | None       | 5                   | 2                 |
| 3  | CS110 class                | 1.5      | Task 2                     | N       | Regular       | 11:00 AM   | 5                   | 2                 |
| 4  | Apply for internship       | 1.0      | None                       | N       | Regular       | None       | 4                   | 3                 |
| 5  | Take shower                | 0.5      | None                       | N       | Regular       | None       | 1                   | 1                 |
| 6  | Tour East Side Gallery     | 2.0      | None                       | N       | City-specific | None       | 1                   | 5                 |
| 7  | Write a reflection of East Side Gallery Tour | 1.0 | Task 6       | N       | City-specific | None       | 1                   | 5                 |
| 8  | CCP meeting with DEGIS     | 0.5      | None                       | N       | City-specific | 1:30 PM    | 5                   | 5                 |

# Task Explanation

### CS110 Class / CCP meeting
- These are tasks with fixed starting times. 
- To assess the functionality of the fixed task priority queue, I deliberately set the utility of the CCP meeting higher than that of the CS110 Class. Since the priority queue for fixed tasks operates based on their starting times, disregarding utility, CS110 Class should be scheduled first by the scheduler.

### CS PCW
- This task represents a non-fixed-timed task that should be completed before a certain fixed-time task (CS110 class), as the latter depends on its completion. This kind of task has the highest utility to place it in the very top of the scheduler in order to prevent a conflict in dependencies (ex. assigned after its dependent fixed time task).
- This task enhances the applicability & versatility of the scheduler, accommodating tasks that lack fixed starting times but still need to be completed before specific events (e.g., cooking before lunch at 11 am).
- If this task cannot be placed before the dependent fixed time task ("CS110 class"), the scheduler will return an error message.

### Tour East Side Gallery
- This task represents a non-fixed time task with dependent non-fixed task (Write a reflection of East Side Gallery Tour), thus having second highest utility among all, after non-fixed time task with fixed task ("CS PCW").

### Write a reflection of East Side Gallery Tour
- This task represents a task that is dependent on non-fixed time task, having second highest utility

### Reading Books / Apply for Internship / Take Shower
- These tasks represent independent tasks with varying levels of academic and career importance, as well as personal interest.
- In a real-world context, these tasks are not dependent, or have tasks dependent on them, so they can be scheduled after fixed-time tasks, and tasks with dependents are assigned to the scheduler.

# Algorithmic Strategy
## Priority Queue
The reasons behind using a priority queue over other data structures are closely related to the nature of the scheduler.

1. A priority queue is better at handling streaming input compared to other data structures like lists. If we are adding a new task to the scheduler, a priority queue can insert new tasks in O(logn) time (for a binary heap implementation), which is more efficient than re-sorting a list every time a new task is added, which would be O(nlogn) for each insertion.
2. When we use a priority queue, the ordering can be based on various criteria, such as utility calculation or starting time. This characteristic is especially important because I am using two heaps with different priority criteria. For the fixed-time task heap, it considers the starting time to determine priority. For the non-fixed-time task heap, it uses utility to determine priority. Likewise, although the tasks fall under the "Task" class, depending on which heap they are in, the ordering criteria change.

# General explanation

My scheduler algorithm works as following:

### Step 1: Define Priority Queues 
I am creating two priority queues, one for fixed-time tasks and one for non-fixed-time tasks.
For fixed-time tasks, the priority within this queue is based on the start time; the earlier the start time, the higher the priority.
For non-fixed-time tasks, the priority in this queue is based on a utility score. The utility score determines the order, with higher scores indicating higher priority.

### Step 2: Populate the Priority Queues for Fixed-Time Tasks
For Fixed-Time Tasks: Place all tasks with a specified start time (tasks that have a "start time" value) into the fixed-time tasks queue, ordered by their start times.

### Step 3. Schedule Fixed-Time Tasks
Get tasks from the fixed-time tasks queue in order of their start times and schedule them into the scheduler.
Check whether it starts after the given starting time. If so, cancel the task.

### Step 4: Populate the Priority Queues for Non-Fixed-Time Tasks based on Utility Equation
Assign a utility score to each task that lacks a specific start time (tasks that do not have a "start time" value) and insert them into the non-fixed-time task queue. Utility calculation is done after scheduling fixed-time tasks as we have to know their priority. The utility score is determined by the formula: 3 * academic_career_importance + 1 * personal_interest + 1000 * sum of priority of fixed tasks dependent on this task + 50 * number of non-fixed tasks dependent on this task. This score reflects the task's importance in terms of academic and career goals, personal interest, and its dependencies on other tasks.

The utility score is designed to prioritize tasks by considering these elements in this following order: 1) sum of dependent fixed tasks' priorities (x1000 weight), 2) number of dependent non-fixed tasks (x50 weight), 3) academic and professional importance(x3 weight), and 4) personal interest (x1 weight). The maximum sum of academic importance and personal interest is 20 (5*3 + 5*1), so the number of dependent non-fixed tasks is more prioritized than academic importance & personal interest.

This also ensures that the flexible task with dependent task to be performed first. For instance, if “CS110 PCW” and “AH112 PCW” are equivalent in terms of dependencies, academic and career importance, and personal interest, the task with a higher priority (earlier start time) dependent fixed task will be prioritized. In other words, if “CS110 class” (dependent on “CS110 PCW”) starts earlier than “AH112 class” (dependent on “AH112 PCW”), “CS110 PCW” will have a higher utility and will be executed first. It's important to note that the sum of priorities is computed such that higher priority tasks receive larger numerical values (e.g., in a scenario with two tasks, the first priority ("CS110 class") is valued at 2 and the second ("AH112 class") at 1). Furthermore, the utility score is based on the number of non-fixed tasks dependent on the tasks; the tasks with more tasks dependent on them should be prioritized to complete the task on time. Lastly, the weight assigned to academic and career importance is greater than personal interest, reflecting my current focus on career development.


### Step 4: Schedule Non-Fixed-Time Tasks
From a given starting time (e.g., 8am), start scheduling non-fixed-time tasks considering the fixed-time tasks. The task with the higher priority (higher utility) will be assigned first in the non-fixed-time tasks queue to the scheduler.

The scheduler finds the earliest available time slot that accommodates the task's duration by checking whether the starting time and ending time of the scheduled task conflicts with the current task. If so, change the starting time of a task to the ending time of the conflicting task, until it finds a time slot that does not conflict with already assigned tasks.

### Step 5: Check Dependencies and Return the Scheduler
Since the prior step does not check whether scheduling non-fixed-time tasks aligns with the dependencies, after scheduling all the tasks, check whether each task's dependencies are completed. If there is no problem, return the final scheduler. If there is any issue in dependency, return the scheduler and state which tasks are conflicting.

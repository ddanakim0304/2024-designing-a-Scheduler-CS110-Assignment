class TaskScheduler:
    """
    A scheduler for organizing tasks based on fixed and flexible timings, dependencies, and priority.
    """
    NOT_STARTED = 'N'
    IN_PRIORITY_QUEUE = 'I'
    COMPLETED = 'C'
    TOO_EARLY = 'E'

    def __init__(self, tasks, starting_time=0):
        """
        Initialize the TaskScheduler with a list of tasks and an optional starting time.

        Parameters
        ----------
        tasks : list
            A list of Task objects to be scheduled.
        starting_time : int, optional
            The starting time for scheduling tasks, by default 0.

        Returns
        -------
        None
        """
 
        self.tasks = {task.id: task for task in tasks}  # Store tasks by ID for easy lookup
        self.fixed_time_tasks = MaxHeapq()
        self.flexible_tasks = MaxHeapq()
        self.comprehensive_schedule = []
        self.starting_time = starting_time  # New attribute to store the scheduler's starting time

    def populate_fixed_time_queues(self):
        """
        Populate the queue for tasks with fixed start times.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        for task in self.tasks.values():
            if task.status == self.NOT_STARTED and task.start_time is not None:
                self.fixed_time_tasks.heappush(task)

    def populate_flexible_time_queues(self):
        """
        Populate the queue for tasks without fixed start times.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        for task in self.tasks.values():
            if task.status == self.NOT_STARTED and task.start_time is None:
                self.flexible_tasks.heappush(task)

    def calculate_utility_scores(self):
        """
        Calculate utility scores for all tasks based on dependencies, academic&career importance, and personal interest.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # Calculate the sum of priorities for tasks that are dependencies of fixed-time tasks
        fixed_task_priorities = {}
        for task in self.tasks.values():
            if task.start_time is not None:
                for dep_id in task.dependencies:
                    if dep_id not in fixed_task_priorities:
                        fixed_task_priorities[dep_id] = task.priority
        # Count the number of non-fixed tasks dependent on each task
        non_fixed_dependents_count = {task_id: 0 for task_id in self.tasks.keys()}
        for task in self.tasks.values():
            if task.start_time is None:
                for dep_id in task.dependencies:
                    non_fixed_dependents_count[dep_id] += 1
        # Adjust utility scores based on the logic
        for task in self.tasks.values():
            dependent_fixed_priority_sum = fixed_task_priorities.get(task.id, 0)
            non_fixed_dependents = non_fixed_dependents_count.get(task.id, 0)
            # Corrected the logical expression and added parentheses for clarity
            task.utility_score = (
                3 * task.academic_career_importance + 
                1 * task.personal_interest + 
                1000 * (dependent_fixed_priority_sum if dependent_fixed_priority_sum is not None else 0) + 
                50 * non_fixed_dependents
            )

    def schedule_fixed_time_tasks(self):
        """
        Schedule all tasks that have fixed start times.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        priority_counter = len(self.fixed_time_tasks)  # Assuming this gives the number of tasks
        while self.fixed_time_tasks.heap_size > 0:
            task = self.fixed_time_tasks.heappop()
            # Check if the task starts before the allowed starting time
            if task.start_time < self.starting_time:
                print(f"🚨🚨 Task '{task.description}' scheduled too early (before starting time), so it is canceled 🚨🚨")
                task.status = self.TOO_EARLY
                continue  # Skip scheduling this task
            task.priority = priority_counter
            # Decrease for the next task
            priority_counter -= 1
            task.scheduled_start_time = task.start_time
            start_time_formatted = f"{task.scheduled_start_time // 60}:{task.scheduled_start_time % 60:02d}"
            print(f"✅ Adding Fixed Schedule... '{task.description}' at {start_time_formatted} for {task.duration} mins.")
            task.status = self.COMPLETED
            end_time = task.scheduled_start_time + task.duration
            self.comprehensive_schedule.append((task.scheduled_start_time, end_time, task.id))
            self.comprehensive_schedule.sort(key=lambda x: x[0])


    def schedule_flexible_tasks(self, starting_time):
        """
        Schedule tasks without fixed start times after considering existing schedules.

        Parameters
        ----------
        starting_time : int
            The starting time from which flexible tasks can be scheduled, written in minute (ex. 8am = 480)

        Returns
        -------
        None
        """
        current_time = starting_time
        self.comprehensive_schedule.sort(key=lambda x: x[0])
        # Ensure the list is sorted by start times for easier conflict detection
        while self.flexible_tasks.heap_size > 0:
            task = self.flexible_tasks.heappop()
            for (start, end, _) in self.comprehensive_schedule:
                # Check for overlap and adjust current_time accordingly
                if current_time < end and current_time + task.duration > start:
                    # Move to the end of the current task
                    current_time = end  
            # Schedule the task at current_time
            task.scheduled_start_time = current_time
            self.comprehensive_schedule.append((current_time, current_time + task.duration, task.id))
            start_time_formatted = f"{current_time // 60}:{current_time % 60:02d}"
            print(f"✅ Adding Flexible Schedule... '{task.description}' at {start_time_formatted} for {task.duration} mins.")
            task.status = self.COMPLETED
            # Prepare for the next task
            current_time += task.duration  

    def dependency_completed_before_task(self, task):
        """
        Check if all dependencies for a task are completed before the task's start time.

        Parameters
        ----------
        task : Task
            The task to check dependencies for.

        Returns
        -------
        bool, str
            A boolean indicating if dependencies are met and a message with details.
        """
        for dep_id in task.dependencies:
            dep_task = self.tasks[dep_id]
            if dep_task.status != self.COMPLETED:
                return False, f"Dependency '{dep_task.description}' (ID: {dep_id}) not completed"
            # Find the dependency's end time in the comprehensive_schedule
            dep_end_time = next((end for start, end, task_id in self.comprehensive_schedule if task_id == dep_id), None)
            if dep_end_time is None or dep_end_time > task.scheduled_start_time:
                return False, f"Dependency '{dep_task.description}' (ID: {dep_id}) ends after task's start time"
        return True, ""  # All dependencies cleared properly

    def display_final_results(self):
        """
        Display the final scheduling results, including any dependency issues.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        print("\n 🌟 Final Task Scheduling Results:\n------------------------------")
        self.comprehensive_schedule.sort(key=lambda x: x[0])  # Ensure it's sorted by start time
        for start_time, end_time, task_id in self.comprehensive_schedule:
            task = self.tasks[task_id]
            all_deps_cleared, conflict_description = self.dependency_completed_before_task(task)
            if not all_deps_cleared:
                print(f"Dependency issue for Task {task.id} ('{task.description}'): {conflict_description}. Please re-check the tasks' input.")
                continue  # Skip printing details for tasks with unmet or untimely dependencies
            start_time_formatted = f"{start_time // 60:02d}:{start_time % 60:02d}"
            end_time_formatted = f"{end_time // 60:02d}:{end_time % 60:02d}"
            status = "Completed" if task.status == self.COMPLETED else "Not Started or In Queue"
            utility = f"Utility Score: {task.utility_score}"
            print(f"{start_time_formatted} - {end_time_formatted}: Task {task.id} ('{task.description}') - {status}, {utility}.")

        # Check if there were any dependency issues at all to provide a final status
        if any(not self.dependency_completed_before_task(task)[0] for task in self.tasks.values()):
            print("⚠️ Some tasks could not be scheduled due to dependency issues. Please re-check the tasks' input.")
        else:
            print("💖 All tasks scheduled successfully with dependencies cleared.")
            starting_time = [start for start, end, task_id in self.comprehensive_schedule][0]
            final_time = [end for start, end, task_id in self.comprehensive_schedule][-1]
            total_time_formatted = f"{(final_time-starting_time) // 60}h {(final_time-starting_time) % 60:02d}min"
            total_utility = sum([task.utility_score for task in self.tasks.values() if task.status == "C"])
            print(f"💖 All the tasks have been completed in {total_time_formatted}, with an overall utility value of {total_utility}")
            
    def run_task_scheduler(self, starting_time=0):
        """
        Execute the scheduling process for all tasks, considering starting time and dependencies.

        Parameters
        ----------
        starting_time : int, optional
            The starting time for scheduling tasks, by default 0.

        Returns
        -------
        None
        """
        # Check if there are no tasks
        if not self.tasks:
            print("No tasks scheduled. Enjoy your day! 🥳 🎉")
            return
        self.starting_time = starting_time
        self.populate_fixed_time_queues()
        self.schedule_fixed_time_tasks()
        self.calculate_utility_scores()
        self.populate_flexible_time_queues()
        self.schedule_flexible_tasks(starting_time)
        self.display_final_results()
        

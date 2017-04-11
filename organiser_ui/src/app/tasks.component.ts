import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute, Params } from '@angular/router';
import { Http } from '@angular/http';

import { Task } from './task';
import { TaskService } from './task.service';
import { PagerService } from "./pager.service";


@Component({
  selector: 'tasks',
  styleUrls: ['./tasks.component.css'],
  templateUrl: './tasks.component.html'
})
export class TasksComponent implements OnInit {
  tasks: Task[];
  displayedTasks: Task[];
  selectedTask: Task;
  subset: string;
  pager: any = {};
  private completedHidden: boolean;
  private tasksCount: number;



  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private http: Http,
    private pagerService: PagerService,
    private taskService: TaskService) {
  }

  ngOnInit(): void {

    this.route.params
      .switchMap((params: Params) => this.getTasks(params['subset']))
      .subscribe(response => {
        this.subset = this.route.snapshot.params['subset'];
        this.tasks = response.results;
        this.displayedTasks = this.tasks;
        this.tasksCount = response.count;
        this.setPage(1);
      })
  }

  onSelect(task: Task): void {
    this.selectedTask = task;
    this.gotoTaskDetails();
  }

  getTasks(subset: string, page?: number): Promise<any> {
    if (subset === 'mine') {
      return this.taskService.getMyTasks(page);
    } else if (subset === 'overdue') {
      return this.taskService.getOverdueTasks(page);
    } else if (subset === 'recent') {
      return this.taskService.getRecentTasks(page);
    } else {
      return this.taskService.getTasks(page);
    }
  }

  gotoTaskDetails(): void {
    this.router.navigate(['/task-detail', this.selectedTask.id])
  }

  hideCompletedTasks(): void {
    this.completedHidden = true;
    this.displayedTasks = this.tasks.filter(task => task.status !== this.taskService.getStatusCode('DONE'));
  }

  showCompletedTasks(): void {
    this.completedHidden = false;
    this.displayedTasks = this.tasks;
  }

  setPage(page: number) {
      if (page < 1 || page > this.pager.totalPages) {
          return;
      }

      this.getTasks(this.subset, page)
          .then(response => {
            this.tasks = response.results;
            this.displayedTasks = this.tasks;
            if (this.completedHidden) {
              this.hideCompletedTasks()
            }
          });

      this.pager = this.pagerService.getPager(this.tasksCount, page);
  }
}

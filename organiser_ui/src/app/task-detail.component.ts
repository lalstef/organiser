import { Component, Input, OnInit } from '@angular/core';
import { ActivatedRoute, Params } from '@angular/router';
import { Location } from '@angular/common';
import 'rxjs/add/operator/switchMap';

import { Task } from './task';
import { TaskService } from './task.service';
import { UserService } from './user.service';

@Component({
  selector: 'task-detail',
  styleUrls: ['./task-detail.component.css'],
  templateUrl: './task-detail.component.html'
})
export class TaskDetailComponent implements OnInit {
  @Input() task: Task;
  editMode: boolean;

  constructor(
    private taskService: TaskService,
    private userService: UserService,
    private route: ActivatedRoute,
    private location: Location
  ) {}

  ngOnInit(): void {
    this.route.params
      .switchMap((params: Params) => this.taskService.getTask(+params['id']))
      .subscribe(task => this.task = task)
  }

  goBack(): void {
    this.location.back();
  }

  markTaskDone(): void {
    this.task.status = this.taskService.getStatusCode('DONE');
    this.saveTask();
  }

  saveTask(): void {
    this.taskService
        .updateTask(this.task)
        .then(task => this.task = task);
    this.exitEditMode();
  }

  enterEditMode(): void {
    this.editMode = true;
  }

  exitEditMode(): void {
    this.editMode = false;
  }

  deleteTask(): void {
    this.taskService
        .deleteTask(this.task)
        .then(() => this.goBack());
  }
}

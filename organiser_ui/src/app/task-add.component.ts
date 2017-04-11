import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { Location } from '@angular/common';

import { Task } from './task';
import { TaskService } from './task.service';

@Component({
  selector: 'task-add',
  styleUrls: ['./task-add.component.css'],
  templateUrl: './task-add.component.html'
})
export class TaskAddComponent {
  task: Task;

  constructor(
    private taskService: TaskService,
    private router: Router,
    private location: Location,
  ) {
    this.task = new Task();
  }

  goBack(): void {
    this.location.back();
  }

  createTask(): void {
    this.taskService
        .createTask(this.task)
        .then(task => this.router.navigate(['/task-detail', task.id]));
  }
}

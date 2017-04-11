import { Injectable } from '@angular/core';
import { Http, RequestOptions, Headers } from '@angular/http';
import 'rxjs/add/operator/toPromise';

import { Task } from './task';
import { UserService } from './user.service';

const TASKS_URL = 'http://localhost:8000/tasks';

  @Injectable()
export class TaskService {

  constructor(private http: Http, private userService: UserService) {}

  getAuthenticationHeaders() {
    let user = this.userService.getCurrentUser(),
      headers = new Headers({'Authorization': `Token ${user.token}`})
    return headers;
  }

  getTask(id: number): Promise<Task> {
    let headers = this.getAuthenticationHeaders(),
      options = new RequestOptions({ headers: headers })
    const url = `${TASKS_URL}/${id}/`;

    return this.http.get(url, options)
      .toPromise()
      .then(response => response.json() as Task)
      .catch(this.handleError);
  }

  getTasks(page: number = 1): Promise<any> {
    let params: URLSearchParams = new URLSearchParams();
    params.set('page', String(page));

    let headers = this.getAuthenticationHeaders(),
      options = new RequestOptions({ headers: headers });

    const url = `${TASKS_URL}/?` + params.toString();

    return this.http.get(url, options)
               .toPromise()
               .then(response => response.json())
               .catch(this.handleError);
  }

  getMyTasks(page: number = 1): Promise<any> {
    let params: URLSearchParams = new URLSearchParams();
    params.set('page', String(page));

    let headers = this.getAuthenticationHeaders(),
      options = new RequestOptions({ headers: headers })

    const url = `${TASKS_URL}/mine/?` + params.toString();

    return this.http.get(url, options)
               .toPromise()
               .then(response => response.json())
               .catch(this.handleError);
  }

  getOverdueTasks(page: number = 1): Promise<any> {
    let params = new URLSearchParams();
    params.set('page', String(page));

    let headers = this.getAuthenticationHeaders(),
      options = new RequestOptions({ headers: headers })

    const url = `${TASKS_URL}/overdue/?` + params.toString();

    return this.http.get(url, options)
               .toPromise()
               .then(response => response.json())
               .catch(this.handleError);
  }

  getRecentTasks(page: number = 1): Promise<any> {
    let headers = this.getAuthenticationHeaders(),
      options = new RequestOptions({ headers: headers });

    let params: URLSearchParams = new URLSearchParams();
    params.set('page', String(page));

    const url = `${TASKS_URL}/recent/?` + params.toString();

    return this.http.get(url, options)
               .toPromise()
               .then(response => response.json())
               .catch(this.handleError);
  }

  markDone(task: Task): Promise<Task> {
    let headers = this.getAuthenticationHeaders(),
      options = new RequestOptions({ headers: headers });

    const url = `${TASKS_URL}/${task.id}/`;

    return this.http.put(url, task, options)
               .toPromise()
               .then(response => response.json())
               .catch(this.handleError);
  }

  updateTask(task: Task): Promise<Task> {
    let headers = this.getAuthenticationHeaders(),
      options = new RequestOptions({ headers: headers })

    const url = `${TASKS_URL}/${task.id}/`;

    return this.http.put(url, task, options)
               .toPromise()
               .then(response => response.json())
               .catch(this.handleError);
  }

  deleteTask(task: Task): Promise<number> {
    let headers = this.getAuthenticationHeaders(),
      options = new RequestOptions({ headers: headers });

    const url = `${TASKS_URL}/${task.id}/`;

    return this.http.delete(url, options)
               .toPromise()
               .then(response => response.json())
               .catch(this.handleError);
  }

  createTask(task: Task): Promise<Task> {
    let headers = this.getAuthenticationHeaders(),
      options = new RequestOptions({ headers: headers })

    const url = `${TASKS_URL}/`;

    return this.http.post(url, task, options)
               .toPromise()
               .then(response => response.json())
               .catch(this.handleError);
  }

  getTaskStatuses() {
    return [
      {value: 0, label: 'NOT_STARTED'},
      {value: 1, label: 'IN_PROGRESS'},
      {value: 2, label: 'DONE'},
      {value: 3, label: 'CANCELLED'}
    ]
  }

  getStatusLabel(code) {
    return {
      0: 'NOT_STARTED',
      1: 'IN_PROGRESS',
      2: 'DONE',
      3: 'CANCELLED'
    }[code];
  }

  getStatusCode(status) {
    return {
      'NOT_STARTED': 0,
      'IN_PROGRESS': 1,
      'DONE': 2,
      'CANCELLED': 3,
    }[status];
  }

  private handleError(error: any): Promise<any> {
    console.error('An error occurred', error);
    return Promise.reject(error.message || error);
  }
}

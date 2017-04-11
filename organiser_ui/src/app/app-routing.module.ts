import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { LoginComponent } from './login.component';
import { DashboardComponent } from './dashboard.component';
import { TasksComponent } from './tasks.component';
import { TaskAddComponent } from './task-add.component';
import { TaskDetailComponent } from './task-detail.component';
import { AuthGuard } from './auth.guard';

const routes: Routes = [
  { path: '', redirectTo: '/dashboard', pathMatch: 'full' },
  { path: 'login', component: LoginComponent },
  { path: 'dashboard', component: DashboardComponent, canActivate: [AuthGuard] },
  { path: 'task-detail/:id', component: TaskDetailComponent, canActivate: [AuthGuard] },
  { path: 'tasks/add', component: TaskAddComponent, canActivate: [AuthGuard] },
  { path: 'tasks/:subset', component: TasksComponent, canActivate: [AuthGuard] },
  { path: 'tasks', component: TasksComponent, canActivate: [AuthGuard] },
];

@NgModule({
  imports: [ RouterModule.forRoot(routes) ],
  exports: [ RouterModule ]
})
export class AppRoutingModule {}

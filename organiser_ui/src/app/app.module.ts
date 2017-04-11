import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpModule } from '@angular/http';

import { ButtonsModule } from 'ngx-bootstrap';

import { AppRoutingModule } from "./app-routing.module";

import { AppComponent } from './app.component';
import { LoginComponent } from './login.component';
import { TasksComponent } from './tasks.component';
import { TaskAddComponent } from "./task-add.component";
import { TaskDetailComponent } from './task-detail.component';
import { DashboardComponent } from "./dashboard.component";

import { TaskService } from './task.service';
import { PagerService } from './pager.service';
import { AuthenticationService } from "./authentication.service";
import { UserService } from "./user.service";
import { AuthGuard } from "./auth.guard";


@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    DashboardComponent,
    TasksComponent,
    TaskAddComponent,
    TaskDetailComponent
  ],
  imports: [
    BrowserModule,
    FormsModule,
    HttpModule,
    AppRoutingModule,
    ButtonsModule.forRoot()
  ],
  providers: [
    TaskService,
    PagerService,
    AuthenticationService,
    UserService,
    AuthGuard
  ],
  bootstrap: [
    AppComponent
  ]
})
export class AppModule { }

import { Component } from '@angular/core';
import { UserService } from "./user.service";
import { AuthenticationService } from "./authentication.service";

@Component({
  selector: 'app-root',
  templateUrl: 'app.component.html',
  styleUrls: ['app.component.css'],
})
export class AppComponent {
  title = 'Organiser';

  constructor(
    private userService: UserService,
    private authenticationService: AuthenticationService
  ) {}
}

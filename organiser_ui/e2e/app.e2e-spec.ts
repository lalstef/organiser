import { OrganiserPage } from './app.po';

describe('organiser App', () => {
  let page: OrganiserPage;

  beforeEach(() => {
    page = new OrganiserPage();
  });

  it('should display message saying app works', () => {
    page.navigateTo();
    expect(page.getParagraphText()).toEqual('app works!');
  });
});

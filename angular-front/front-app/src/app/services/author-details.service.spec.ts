import { TestBed } from '@angular/core/testing';

import { AuthorDetailsService } from './author-details.service';

describe('AuthorDetailsService', () => {
  let service: AuthorDetailsService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(AuthorDetailsService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});

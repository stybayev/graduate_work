insert into movie.film_work (id, title, imdb_rating, description, genre, actors_names, writers_names, director, created)
values ('4254661e-89bd-42f3-8644-0ce55fc8375b', 'Тени исчезают в полдень', 5.6, 'Тень исчезла ровно в полдень',
ARRAY['comedy', 'thriller'], ARRAY['Jhonny', 'Sara Jessica Parker'], ARRAY['Jhon CLun'], 'Gay Ritchi', CURRENT_DATE) ON CONFLICT DO NOTHING;

insert into movie.film_work (id, title, imdb_rating, description, genre, actors_names, writers_names, director, created)
values ('67cc9f09-b1cb-48b5-9966-9aefa35ada01', 'Все псы попадают в рай', 9.6, 'Собака попала в рай для собак',
ARRAY['horror', 'thriller'], ARRAY['Jhonny', 'Sara Jessica Parker'], ARRAY['Jhon CLun'], 'Gay Ritchi', CURRENT_DATE) ON CONFLICT DO NOTHING;

insert into movie.film_work (id, title, imdb_rating, description, genre, actors_names, writers_names, director, created)
values ('e4bcb063-646e-459d-a815-9facc31357a8', '1+1', 3.1, 'Фильм про любовь и не только',
ARRAY['comedy', 'drama'], ARRAY['Jhonny', 'Sara Jessica Parker'], ARRAY['Jhon CLun'], 'Gay Ritchi', CURRENT_DATE) ON CONFLICT DO NOTHING;

insert into movie.film_work (id, title, imdb_rating, description, genre, actors_names, writers_names, director, created)
values ('8b48a9d0-83aa-464f-af71-8bc04d47210f', 'Хроники Риддика', 8.5, 'Описание фильма',
ARRAY['comedy'], ARRAY['Jhonny', 'Sara Jessica Parker'], ARRAY['Jhon CLun'], 'Gay Ritchi', CURRENT_DATE) ON CONFLICT DO NOTHING;

insert into movie.film_work (id, title, imdb_rating, description, genre, actors_names, writers_names, director, created)
values ('95868fc3-573a-49a8-b96d-a3b3c378c3f3', 'Алладин', 1.1, 'Магия Джинна',
ARRAY['music', 'thriller'], ARRAY['Jhonny', 'Sara Jessica Parker'], ARRAY['Jhon CLun'], 'Gay Ritchi', CURRENT_DATE) ON CONFLICT DO NOTHING;
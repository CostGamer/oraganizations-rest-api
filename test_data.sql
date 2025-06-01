BEGIN;

-- можно оптимизировать реализивов m2m между потенциальными таблицами buildings & offices
INSERT INTO buildings (address, office, location) VALUES
    ('г. Москва, ул. Ленина 1', 1, ST_SetSRID(ST_MakePoint(37.620393, 55.75396), 4326)),
    ('г. Москва, ул. Ленина 1', 2, ST_SetSRID(ST_MakePoint(37.620393, 55.75396), 4326)),
    ('г. Москва, ул. Ленина 1', 3, ST_SetSRID(ST_MakePoint(37.620393, 55.75396), 4326)),
    ('г. Санкт-Петербург, Невский проспект 30', 1, ST_SetSRID(ST_MakePoint(30.335098, 59.9342802), 4326)),
    ('г. Санкт-Петербург, Невский проспект 30', 2, ST_SetSRID(ST_MakePoint(30.335098, 59.9342802), 4326)),
    ('г. Новосибирск, Красный проспект 50', 1, ST_SetSRID(ST_MakePoint(82.92043, 55.030199), 4326)),
    ('г. Новосибирск, Красный проспект 50', 2, ST_SetSRID(ST_MakePoint(82.92043, 55.030199), 4326)),
    ('г. Екатеринбург, ул. Малышева 1', 1, ST_SetSRID(ST_MakePoint(60.6105, 56.8389), 4326)),
    ('г. Казань, ул. Баумана 10', 1, ST_SetSRID(ST_MakePoint(49.1221, 55.7887), 4326)),
    ('г. Нижний Новгород, ул. Минина 5', 1, ST_SetSRID(ST_MakePoint(44.0020, 56.3287), 4326)),
    ('г. Москва, ул. Тверская 7', 10, ST_SetSRID(ST_MakePoint(37.605602, 55.757408), 4326)),
    ('г. Москва, Красная площадь 1', 5, ST_SetSRID(ST_MakePoint(37.620795, 55.754093), 4326));


INSERT INTO organizations (name, building_id)
VALUES
    ('ООО Рога и Копыта', (SELECT id FROM buildings WHERE address = 'г. Москва, ул. Ленина 1' AND office = 1)),
    ('ЗАО Умные Решения', (SELECT id FROM buildings WHERE address = 'г. Москва, ул. Ленина 1' AND office = 2)),
    ('ИП Колбаскин', (SELECT id FROM buildings WHERE address = 'г. Москва, ул. Ленина 1' AND office = 3)),
    ('ООО Питерская Классика', (SELECT id FROM buildings WHERE address = 'г. Санкт-Петербург, Невский проспект 30' AND office = 1)),
    ('ЗАО Невские Берега', (SELECT id FROM buildings WHERE address = 'г. Санкт-Петербург, Невский проспект 30' AND office = 2)),
    ('ООО Сибирские Технологии', (SELECT id FROM buildings WHERE address = 'г. Новосибирск, Красный проспект 50' AND office = 1)),
    ('ИП Новосибирская Мечта', (SELECT id FROM buildings WHERE address = 'г. Новосибирск, Красный проспект 50' AND office = 2)),
    ('ООО УралСтрой', (SELECT id FROM buildings WHERE address = 'г. Екатеринбург, ул. Малышева 1' AND office = 1)),
    ('ЗАО Казанские Продукты', (SELECT id FROM buildings WHERE address = 'г. Казань, ул. Баумана 10' AND office = 1)),
    ('ИП Нижегородская Кулинария', (SELECT id FROM buildings WHERE address = 'г. Нижний Новгород, ул. Минина 5' AND office = 1)),
    ('ИП Moscow Dynamics', (SELECT id FROM buildings WHERE address = 'г. Москва, ул. Тверская 7' AND office = 10)),
    ('ИП Innovatech Solutions', (SELECT id FROM buildings WHERE address = 'г. Москва, Красная площадь 1' AND office = 5));


INSERT INTO phones (phone_number)
VALUES
    ('2-222-222'),
    ('3-333-333'),
    ('4-444-444'),
    ('5-555-555'),
    ('6-666-666'),
    ('8-923-666-13-13'),
    ('8-800-555-35-35'),
    ('8-495-123-45-67'),
    ('8-499-987-65-43'),
    ('8-800-123-45-67'),
    ('7-911-111-11-11'),
    ('8-921-234-56-78'),
    ('8-495-433-45-67'),
    ('8-499-333-65-43'),
    ('8-800-444-45-67'),
    ('7-911-000-11-11'),
    ('8-921-999-56-78'),
    ('8-800-555-12-12'),
    ('7-988-999-56-78'),
    ('7-888-555-12-12');


INSERT INTO organization_phones (phone_number_id, organization_id)
VALUES
    ((SELECT id FROM phones WHERE phone_number = '2-222-222'), (SELECT id FROM organizations WHERE name = 'ООО Рога и Копыта')),
    ((SELECT id FROM phones WHERE phone_number = '3-333-333'), (SELECT id FROM organizations WHERE name = 'ООО Рога и Копыта')),
    ((SELECT id FROM phones WHERE phone_number = '6-666-666'), (SELECT id FROM organizations WHERE name = 'ООО Рога и Копыта')),
    ((SELECT id FROM phones WHERE phone_number = '4-444-444'), (SELECT id FROM organizations WHERE name = 'ЗАО Умные Решения')),
    ((SELECT id FROM phones WHERE phone_number = '5-555-555'), (SELECT id FROM organizations WHERE name = 'ЗАО Умные Решения')),
    ((SELECT id FROM phones WHERE phone_number = '8-923-666-13-13'), (SELECT id FROM organizations WHERE name = 'ИП Колбаскин')),
    ((SELECT id FROM phones WHERE phone_number = '8-800-555-35-35'), (SELECT id FROM organizations WHERE name = 'ИП Колбаскин')),
    ((SELECT id FROM phones WHERE phone_number = '8-495-123-45-67'), (SELECT id FROM organizations WHERE name = 'ООО Питерская Классика')),
    ((SELECT id FROM phones WHERE phone_number = '8-499-987-65-43'), (SELECT id FROM organizations WHERE name = 'ЗАО Невские Берега')),
    ((SELECT id FROM phones WHERE phone_number = '8-800-123-45-67'), (SELECT id FROM organizations WHERE name = 'ООО Сибирские Технологии')),
    ((SELECT id FROM phones WHERE phone_number = '7-911-111-11-11'), (SELECT id FROM organizations WHERE name = 'ИП Новосибирская Мечта')),
    ((SELECT id FROM phones WHERE phone_number = '8-921-234-56-78'), (SELECT id FROM organizations WHERE name = 'ООО УралСтрой')),
    ((SELECT id FROM phones WHERE phone_number = '8-495-433-45-67'), (SELECT id FROM organizations WHERE name = 'ЗАО Казанские Продукты')),
    ((SELECT id FROM phones WHERE phone_number = '8-499-333-65-43'), (SELECT id FROM organizations WHERE name = 'ИП Нижегородская Кулинария')),
    ((SELECT id FROM phones WHERE phone_number = '7-988-999-56-78'), (SELECT id FROM organizations WHERE name = 'ИП Moscow Dynamics')),
    ((SELECT id FROM phones WHERE phone_number = '7-888-555-12-12'), (SELECT id FROM organizations WHERE name = 'ИП Innovatech Solutions'));


INSERT INTO activities (name)
VALUES
    ('Еда'),
    ('Мясная продукция'),
    ('Молочная продукция'),
    ('Напитки'),
    ('Соки'),
    ('Алкогольные напитки'),
    ('Вина'),
    ('Крепкий алкоголь'),
    ('Автомобили'),
    ('Легковые'),
    ('Запчасти'),
    ('Аксессуары'),
    ('Спорттовары'),
    ('Композитные спорттовары');


INSERT INTO activity_closure (ancestor_id, descendant_id)
VALUES
    ((SELECT id FROM activities WHERE name = 'Еда'), (SELECT id FROM activities WHERE name = 'Еда')),
    ((SELECT id FROM activities WHERE name = 'Еда'), (SELECT id FROM activities WHERE name = 'Мясная продукция')),
    ((SELECT id FROM activities WHERE name = 'Еда'), (SELECT id FROM activities WHERE name = 'Молочная продукция')),
    ((SELECT id FROM activities WHERE name = 'Еда'), (SELECT id FROM activities WHERE name = 'Напитки')),
    ((SELECT id FROM activities WHERE name = 'Еда'), (SELECT id FROM activities WHERE name = 'Соки')),
    ((SELECT id FROM activities WHERE name = 'Еда'), (SELECT id FROM activities WHERE name = 'Алкогольные напитки')),
    ((SELECT id FROM activities WHERE name = 'Еда'), (SELECT id FROM activities WHERE name = 'Вина')),
    ((SELECT id FROM activities WHERE name = 'Еда'), (SELECT id FROM activities WHERE name = 'Крепкий алкоголь')),
    ((SELECT id FROM activities WHERE name = 'Мясная продукция'), (SELECT id FROM activities WHERE name = 'Мясная продукция')),
    ((SELECT id FROM activities WHERE name = 'Молочная продукция'), (SELECT id FROM activities WHERE name = 'Молочная продукция')),
    ((SELECT id FROM activities WHERE name = 'Напитки'), (SELECT id FROM activities WHERE name = 'Напитки')),
    ((SELECT id FROM activities WHERE name = 'Напитки'), (SELECT id FROM activities WHERE name = 'Соки')),
    ((SELECT id FROM activities WHERE name = 'Напитки'), (SELECT id FROM activities WHERE name = 'Алкогольные напитки')),
    ((SELECT id FROM activities WHERE name = 'Напитки'), (SELECT id FROM activities WHERE name = 'Вина')),
    ((SELECT id FROM activities WHERE name = 'Напитки'), (SELECT id FROM activities WHERE name = 'Крепкий алкоголь')),
    ((SELECT id FROM activities WHERE name = 'Алкогольные напитки'), (SELECT id FROM activities WHERE name = 'Вина')),
    ((SELECT id FROM activities WHERE name = 'Алкогольные напитки'), (SELECT id FROM activities WHERE name = 'Крепкий алкоголь')),
    ((SELECT id FROM activities WHERE name = 'Вина'), (SELECT id FROM activities WHERE name = 'Вина')),
    ((SELECT id FROM activities WHERE name = 'Крепкий алкоголь'), (SELECT id FROM activities WHERE name = 'Крепкий алкоголь')),
    ((SELECT id FROM activities WHERE name = 'Соки'), (SELECT id FROM activities WHERE name = 'Соки')),

    ((SELECT id FROM activities WHERE name = 'Автомобили'), (SELECT id FROM activities WHERE name = 'Автомобили')),
    ((SELECT id FROM activities WHERE name = 'Автомобили'), (SELECT id FROM activities WHERE name = 'Легковые')),
    ((SELECT id FROM activities WHERE name = 'Автомобили'), (SELECT id FROM activities WHERE name = 'Запчасти')),
    ((SELECT id FROM activities WHERE name = 'Автомобили'), (SELECT id FROM activities WHERE name = 'Аксессуары')),
    ((SELECT id FROM activities WHERE name = 'Легковые'), (SELECT id FROM activities WHERE name = 'Легковые')),
    ((SELECT id FROM activities WHERE name = 'Легковые'), (SELECT id FROM activities WHERE name = 'Запчасти')),
    ((SELECT id FROM activities WHERE name = 'Легковые'), (SELECT id FROM activities WHERE name = 'Аксессуары')),
    ((SELECT id FROM activities WHERE name = 'Запчасти'), (SELECT id FROM activities WHERE name = 'Запчасти')),
    ((SELECT id FROM activities WHERE name = 'Аксессуары'), (SELECT id FROM activities WHERE name = 'Аксессуары')),

    ((SELECT id FROM activities WHERE name = 'Спорттовары'), (SELECT id FROM activities WHERE name = 'Композитные спорттовары')),
    ((SELECT id FROM activities WHERE name = 'Спорттовары'), (SELECT id FROM activities WHERE name = 'Композитные спорттовары')),
    ((SELECT id FROM activities WHERE name = 'Композитные спорттовары'), (SELECT id FROM activities WHERE name = 'Композитные спорттовары'));


INSERT INTO organization_activities (organization_id, activity_id)
VALUES
    ((SELECT id FROM organizations WHERE name = 'ООО Рога и Копыта'), (SELECT id FROM activities WHERE name = 'Еда')),
    ((SELECT id FROM organizations WHERE name = 'ООО Рога и Копыта'), (SELECT id FROM activities WHERE name = 'Мясная продукция')),
    ((SELECT id FROM organizations WHERE name = 'ООО Рога и Копыта'), (SELECT id FROM activities WHERE name = 'Молочная продукция')),
    ((SELECT id FROM organizations WHERE name = 'ЗАО Умные Решения'), (SELECT id FROM activities WHERE name = 'Напитки')),
    ((SELECT id FROM organizations WHERE name = 'ЗАО Умные Решения'), (SELECT id FROM activities WHERE name = 'Соки')),
    ((SELECT id FROM organizations WHERE name = 'ИП Колбаскин'), (SELECT id FROM activities WHERE name = 'Алкогольные напитки')),
    ((SELECT id FROM organizations WHERE name = 'ИП Колбаскин'), (SELECT id FROM activities WHERE name = 'Вина')),
    ((SELECT id FROM organizations WHERE name = 'ООО Питерская Классика'), (SELECT id FROM activities WHERE name = 'Крепкий алкоголь')),
    ((SELECT id FROM organizations WHERE name = 'ЗАО Невские Берега'), (SELECT id FROM activities WHERE name = 'Автомобили')),
    ((SELECT id FROM organizations WHERE name = 'ЗАО Невские Берега'), (SELECT id FROM activities WHERE name = 'Легковые')),
    ((SELECT id FROM organizations WHERE name = 'ООО Сибирские Технологии'), (SELECT id FROM activities WHERE name = 'Запчасти')),
    ((SELECT id FROM organizations WHERE name = 'ИП Новосибирская Мечта'), (SELECT id FROM activities WHERE name = 'Аксессуары')),
    ((SELECT id FROM organizations WHERE name = 'ООО УралСтрой'), (SELECT id FROM activities WHERE name = 'Еда')),
    ((SELECT id FROM organizations WHERE name = 'ЗАО Казанские Продукты'), (SELECT id FROM activities WHERE name = 'Еда')),
    ((SELECT id FROM organizations WHERE name = 'ЗАО Казанские Продукты'), (SELECT id FROM activities WHERE name = 'Молочная продукция')),
    ((SELECT id FROM organizations WHERE name = 'ИП Нижегородская Кулинария'), (SELECT id FROM activities WHERE name = 'Мясная продукция')),
    ((SELECT id FROM organizations WHERE name = 'ИП Moscow Dynamics'), (SELECT id FROM activities WHERE name = 'Спорттовары')),
    ((SELECT id FROM organizations WHERE name = 'ИП Innovatech Solutions'), (SELECT id FROM activities WHERE name = 'Композитные спорттовары'));

COMMIT;
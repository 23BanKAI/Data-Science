workspace {

    model {
        user = Person "Пользователь" "Добавляет услугу в заказ"
        
        system = SoftwareSystem "Система заказа услуг" {
            webapp = Container "Веб-приложение" "React" "Взаимодействие с пользователем"
            backend = Container "Backend API" "Spring Boot" "Управление пользователями и заказами"
            database = Container "База данных" "PostgreSQL" "Хранение информации"
            
            user -> webapp "Использует для взаимодействия с системой"
            webapp -> backend "Отправка запросов"
            backend -> database "Хранение данных"
        }
    }

    views {
        systemContext system {
            include *
            autolayout lr
        }

        dynamic system {
            user -> webapp "Запрос добавления услуги"
            webapp -> backend "Отправка API-запроса"
            backend -> database "Сохранение данных заказа"
            autolayout lr
        }

        theme default
    }
}

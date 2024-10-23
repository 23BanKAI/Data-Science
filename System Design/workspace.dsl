workspace {

    model {
        user = Person "Пользователь" "Добавляет услугу в заказ"

        userContext = SoftwareSystem "Контекст управления пользователями" "Работа с пользователями" {
            userAggregate = Container "Агрегат Пользователь" "Управляет данными пользователя" "Spring Boot"
        }

        serviceContext = SoftwareSystem "Контекст управления услугами" "Работа с каталогом услуг" {
            serviceAggregate = Container "Агрегат Услуга" "Управляет данными услуги" "Spring Boot"
        }

        orderContext = SoftwareSystem "Контекст управления заказами" "Работа с заказами" {
            orderAggregate = Container "Агрегат Заказ" "Управляет данными заказа" "Spring Boot"
        }

        // Система
        system = SoftwareSystem "Система заказа услуг" {
            webapp = Container "Веб-приложение" "React" "Взаимодействие с пользователем"
            database = Container "База данных" "PostgreSQL" "Хранение информации"
            
            // Взаимодействие пользователя с системой
            user -> webapp "Использует для взаимодействия с системой"
            webapp -> userAggregate "Отправка запросов к агрегату пользователя"
            webapp -> serviceAggregate "Запросы на получение услуг"
            webapp -> orderAggregate "Запросы на создание заказа"
            database -> userAggregate "Хранение данных о пользователе"
            database -> serviceAggregate "Хранение данных об услугах"
            database -> orderAggregate "Хранение данных о заказах"
        }
    }

    views {
        systemContext system {
            include *
            autolayout lr
        }

        dynamic system {
            user -> webapp "Запрос добавления услуги"
            webapp -> userAggregate "Создание/поиск пользователя"
            webapp -> serviceAggregate "Получение услуг"
            webapp -> orderAggregate "Создание заказа"
            autolayout lr
        }

        theme default
    }
}

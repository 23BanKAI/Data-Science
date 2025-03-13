workspace {

    model {
        user = Person "Пользователь" "Добавляет услугу в заказ"

        userContext = SoftwareSystem "Контекст управления пользователями" "Работа с пользователями" {
            userAggregate = Container "Агрегат Пользователь" "Управляет данными пользователя" "FastAPI"
        }

        serviceContext = SoftwareSystem "Контекст управления услугами" "Работа с каталогом услуг" {
            serviceAggregate = Container "Агрегат Услуга" "Управляет данными услуги" "FastAPI"
        }

        orderContext = SoftwareSystem "Контекст управления заказами" "Работа с заказами" {
            orderAggregate = Container "Агрегат Заказ" "Управляет данными заказа" "FastAPI"
        }

        // Система
        system = SoftwareSystem "Система заказа услуг" {
            api = Container "API" "FastAPI" "Обработка запросов от пользователей"
            database = Container "База данных" "PostgreSQL" "Хранение информации"
            
            // Взаимодействие пользователя с системой
            user -> api "Использует для взаимодействия с системой"
            api -> userAggregate "Отправка запросов к агрегату пользователя"
            api -> serviceAggregate "Запросы на получение услуг"
            api -> orderAggregate "Запросы на создание заказа"
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
            user -> api "Запрос добавления услуги"
            api -> userAggregate "Создание/поиск пользователя"
            api -> serviceAggregate "Получение услуг"
            api -> orderAggregate "Создание заказа"
            autolayout lr
        }

        theme default
    }
}

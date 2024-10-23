workspace {

    model {
        user = Person "Пользователь" "Добавляет услугу в заказ"
        
        // Ограниченные контексты
        userContext = SoftwareSystem "Контекст управления пользователями" "Работа с пользователями"
        serviceContext = SoftwareSystem "Контекст управления услугами" "Работа с каталогом услуг"
        orderContext = SoftwareSystem "Контекст управления заказами" "Работа с заказами и их обработкой"

        // Система и контейнеры
        system = SoftwareSystem "Система заказа услуг" {
            webapp = Container "Веб-приложение" "React" "Взаимодействие с пользователем"
            backend = Container "Backend API" "Spring Boot" "Управление пользователями, услугами и заказами"
            database = Container "База данных" "PostgreSQL" "Хранение информации"
            
            // Взаимодействие пользователя с системой
            user -> webapp "Использует для взаимодействия с системой"
            webapp -> backend "Отправка запросов"
            backend -> database "Хранение данных"
        }
        
        // Связи с ограниченными контекстами
        backend -> userContext "Управление пользователями"
        backend -> serviceContext "Управление услугами"
        backend -> orderContext "Управление заказами"
    }

    views {
        // Диаграмма контекста системы
        systemContext system {
            include *
            autolayout lr
        }

        // Динамическая диаграмма
        dynamic system {
            user -> webapp "Запрос добавления услуги"
            webapp -> backend "Отправка API-запроса"
            backend -> database "Сохранение данных заказа"
            autolayout lr
        }

        theme default
    }
}

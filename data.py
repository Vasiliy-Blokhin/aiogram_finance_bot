def start_message(name):
    hello_message = (
        f'Приветсвую, {name}!\n\n Если тебе понравился бот и ты хочешь, чтобы '
        'я улучшал его, то дай обратную связь: \n ---> @Vasilianin.\n\n'
    )
    disclaimer_message = (
        'Дисклеймер:\n Результат, который выдает бот может '
        'быть ошибочным, так как данные берутся со сторонних сервисов.\n Акции'
        ' подбираются согласно различных мультипликаторов и на основе их '
        'выдаются рекомендации.\n Дальнейшие действия на ваш риск. '
        '\n\nНа данный момент бот находится в разработке, так что возможны '
        'отключения, сбои, неверная информация.'
    )
    return hello_message + disclaimer_message
async def city_check(locations, text='📍 Адреси, за якими ви можете нас знайти 📍\n\n'):
    count = 1
    for location in locations:
        text += f'{count}. {location.address}\n👉 <a href="{location.maps_url}">Перейти до Google Maps</a>\n\n' 
        count += 1
    
    return text
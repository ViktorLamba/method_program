import requests
import matplotlib.pyplot as plt
import numpy as np
from typing import Dict, List

# ========== 1. ПОЛУЧЕНИЕ ДАННЫХ ==========
base_url = 'https://pokeapi.co/api/v2/'
limit = 10
url = f'{base_url}pokemon?limit={limit}'

print("🔄 Загружаем данные о покемонах...")
response = requests.get(url)
pokemon_list = response.json()['results']

data: List[Dict] = []

for pokemon in pokemon_list:
    print(f"📥 Загружаем {pokemon['name']}...")
    
    # Получаем детальную информацию о покемоне
    pokemon_url = pokemon['url']
    pokemon_response = requests.get(pokemon_url)
    pokemon_data = pokemon_response.json()
    
    # Извлекаем характеристики
    pokemon_dict = {
        'id': pokemon_data['id'],
        'name': pokemon_data['name'].title(),
        'height': pokemon_data['height'] / 10,  # в метрах
        'weight': pokemon_data['weight'] / 10,  # в кг
        'hp': pokemon_data['stats'][0]['base_stat'],  # HP
        'attack': pokemon_data['stats'][1]['base_stat'],
        'defense': pokemon_data['stats'][2]['base_stat'],
        # Дополнительные характеристики
        'speed': pokemon_data['stats'][5]['base_stat'],
        'special_attack': pokemon_data['stats'][3]['base_stat'],
        'total_stats': sum(stat['base_stat'] for stat in pokemon_data['stats'])
    }
    
    data.append(pokemon_dict)

print(f"✅ Загружено {len(data)} покемонов!")


# Подготовка данных для графиков
names = [p['name'] for p in data]
hp = [p['hp'] for p in data]
attack = [p['attack'] for p in data]
defense = [p['defense'] for p in data]
weights = [p['weight'] for p in data]
total_stats = [p['total_stats'] for p in data]
ids = [p['id'] for p in data]

plt.style.use('dark_background')
fig = plt.figure(figsize=(20, 24))

# ========== 1. Линейный график ==========
plt.subplot(3, 2, 1)
plt.plot(ids, hp, 'o-', linewidth=3, markersize=10, color='#ff6b6b', label='HP')
plt.plot(ids, attack, 's-', linewidth=3, markersize=10, color='#4ecdc4', label='Attack')
plt.plot(ids, defense, '^-', linewidth=3, markersize=10, color='#45b7d1', label='Defense')
plt.title('Зависимость характеристик от ID покемона', fontsize=14, fontweight='bold', pad=20)
plt.xlabel('ID покемона')
plt.ylabel('Характеристики')
plt.legend()
plt.grid(True, alpha=0.3)
plt.xticks(rotation=45)

# ========== 2. Точечная диаграмма ==========
plt.subplot(3, 2, 2)
sizes = np.array(attack) * 8  # размер точек
plt.scatter(weights, hp, s=sizes, c=total_stats, cmap='viridis', alpha=0.7, edgecolors='white', linewidth=1.5)
plt.colorbar(label='Общие статы')
for i, name in enumerate(names):
    plt.annotate(name, (weights[i], hp[i]), xytext=(5, 5), textcoords='offset points', fontsize=9)
plt.title('HP vs Вес (размер = Attack)', fontsize=14, fontweight='bold', pad=20)
plt.xlabel('Вес (кг)')
plt.ylabel('HP')


# ========== 3. Столбчатая диаграмма ==========
plt.subplot(3, 2, 3)
x = np.arange(len(names))
width = 0.25

plt.bar(x - width, hp, width, label='HP', color='#ff6b6b', alpha=0.8)
plt.bar(x, attack, width, label='Attack', color='#4ecdc4', alpha=0.8)
plt.bar(x + width, defense, width, label='Defense', color='#45b7d1', alpha=0.8)

plt.title('Сравнение характеристик покемонов', fontsize=14, fontweight='bold', pad=20)
plt.xlabel('Покемоны')
plt.ylabel('Характеристики')
plt.xticks(x, names, rotation=45, ha='right')
plt.legend()
plt.grid(True, alpha=0.3, axis='y')

# ========== 4. Горизонтальная столбчатая диаграмма ==========
plt.subplot(3, 2, 4)
plt.barh(names[::-1], total_stats[::-1], color='gold', alpha=0.8)
plt.title('Общие статы покемонов (горизонтально)', fontsize=14, fontweight='bold', pad=20)
plt.xlabel('Общие статы')
plt.ylabel('Покемоны')
for i, v in enumerate(total_stats[::-1]):
    plt.text(v + 5, i, str(v), va='center', fontweight='bold')

# ========== 5. Гистограмма ==========
plt.subplot(3, 2, 5)
plt.hist([hp, attack, defense], bins=5, label=['HP', 'Attack', 'Defense'], 
         alpha=0.7, edgecolor='white', linewidth=2)
plt.title('Распределение характеристик', fontsize=14, fontweight='bold', pad=20)
plt.xlabel('Значение характеристики')
plt.ylabel('Количество покемонов')
plt.legend()
plt.grid(True, alpha=0.3)

# ========== 6. Круговая диаграмма ==========
plt.subplot(3, 2, 6)
sizes = [p['hp'] + p['attack'] + p['defense'] for p in data]
colors = plt.cm.Set3(np.linspace(0, 1, len(names)))
plt.pie(sizes, labels=names, colors=colors, autopct='%1.1f%%', startangle=90)
plt.title('Доля характеристик каждого покемона', fontsize=14, fontweight='bold', pad=20)

plt.tight_layout()
plt.suptitle('🐉 Анализ характеристик покемонов 🐉', fontsize=20, fontweight='bold', y=0.98)
plt.show()

# ========== 3. ВЫВОД ДАННЫХ ==========
print("\n" + "="*60)
print("📊 СОБРАННЫЕ ДАННЫЕ:")
print("="*60)
for pokemon in data:
    print(f"ID: {pokemon['id']:2d} | {pokemon['name']:12s} | "
          f"HP: {pokemon['hp']:3d} | ATK: {pokemon['attack']:3d} | "
          f"DEF: {pokemon['defense']:3d} | Вес: {pokemon['weight']:5.1f}кг")

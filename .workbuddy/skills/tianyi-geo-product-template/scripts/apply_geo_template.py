# -*- coding: utf-8 -*-
import json, re
from pathlib import Path

BASE = Path('E:/赵雯/独立站/Kim网站/tianyi-site')

CSS_ANCHOR = '.feature-item p { font-size:13px; color:var(--text-muted); margin:0; }'
FAQ_CSS = '''
/* FAQ (GEO template) */
.faq-list { margin-top:8px; }
.faq-item { border:1px solid var(--border); border-radius:10px; padding:18px 20px; margin-bottom:14px; background:#fff; }
.faq-item h3 { font-size:16px; color:var(--primary); margin-bottom:8px; line-height:1.4; }
.faq-item p { margin:0; font-size:14px; color:var(--text-muted); }'''

CTA_ANCHOR = '<section class="container">\n  <div class="cta-box">'

CONFIG = {
  'belt-conveyor': {
    'en': {
      'props': [
        ['Model Series', 'TD75, DTII, DTII(A), DX'],
        ['Belt Width', '500 - 2000 mm'],
        ['Capacity', '45 - 2,000 t/h'],
        ['Belt Speed', '0.8 - 5.0 m/s'],
        ['Max Inclination', 'Up to 18 deg (28 deg with chevron belt)'],
        ['Frame Material', 'Carbon steel (standard), stainless steel (optional)'],
      ],
      'faq': [
        ['What is a belt conveyor and what is it used for?',
         'A belt conveyor uses a continuous moving belt to transport bulk materials over long distances at high capacity. It is widely used for coal, ore, aggregates, cement, grain, and other free-flowing solids in mining, power, port, and cement industries.'],
        ['What belt widths and capacities are available?',
         'Belt widths range from 500 to 2000 mm, with capacities from 45 to 2,000 t/h depending on belt speed (0.8-5.0 m/s) and material. Larger widths and speeds deliver higher throughput.'],
        ['What is the maximum inclination for a belt conveyor?',
         'Standard troughed belt conveyors handle inclinations up to about 18 degrees. With chevron (patterned) belts, the angle can reach up to 28 degrees for loose, non-slip materials.'],
        ['What belt and frame materials are offered?',
         'Belts include rubber (EP/NN/ST), PVC, PU, and heat-, oil-, or flame-resistant grades. Frames are carbon steel as standard, with stainless steel optional for food and chemical applications.'],
        ['How does a belt conveyor compare to a chain or screw conveyor?',
         'Belt conveyors are best for long-distance, high-speed transport of low-abrasive bulk solids. Chain and screw conveyors are better for sealed, dust-tight handling, multiple inlets and outlets, and abrasive or hazardous materials.'],
      ],
    },
    'ru': {
      'props': [
        ['Серия моделей', 'TD75, DTII, DTII(A), DX'],
        ['Ширина ленты', '500 - 2000 мм'],
        ['Производительность', '45 - 2 000 т/ч'],
        ['Скорость ленты', '0,8 - 5,0 м/с'],
        ['Макс. угол наклона', 'до 18° (до 28° с рифлёной лентой)'],
        ['Материал рамы', 'углеродистая сталь (стандарт), нержавеющая сталь (опция)'],
      ],
      'faq': [
        ['Что такое ленточный конвейер и для чего он используется?',
         'Ленточный конвейер использует непрерывно движущуюся ленту для транспортировки сыпучих материалов на большие расстояния с высокой производительностью. Широко применяется для угля, руды, щебня, цемента, зерна и других сыпучих грузов в горной, энергетической, портовой и цементной отраслях.'],
        ['Какие ширина ленты и производительность доступны?',
         'Ширина ленты составляет от 500 до 2000 мм, производительность - от 45 до 2 000 т/ч в зависимости от скорости ленты (0,8-5,0 м/с) и материала. Большие ширина и скорость обеспечивают большую пропускную способность.'],
        ['Каков максимальный угол наклона ленточного конвейера?',
         'Стандартные желобчатые ленточные конвейеры работают при наклоне до 18 градусов. С рифлёной (шевронной) лентой угол может достигать 28 градусов для сыпучих нескользящих материалов.'],
        ['Из каких материалов изготавливаются лента и рама?',
         'Ленты: резиновые (EP/NN/ST), PVC, PU, а также термо-, масло- и пламостойкие. Рамы - углеродистая сталь (стандарт), нержавеющая сталь (опция) для пищевой и химической отраслей.'],
        ['Чем ленточный конвейер отличается от цепного или шнекового?',
         'Ленточные конвейеры лучше всего подходят для транспортировки на большие расстояния с высокой скоростью малонабразивных сыпучих материалов. Цепные и шнековые конвейеры предпочтительнее для герметичной беспыльной подачи, нескольких точек загрузки и выгрузки, а также абразивных или опасных материалов.'],
      ],
    },
  },
  'screw-conveyor': {
    'en': {
      'props': [
        ['Model Series', 'LS (standard), GX (pipe type), LC (vertical)'],
        ['Screw Diameter', '100 - 1250 mm'],
        ['Capacity', '1 - 300 m3/h'],
        ['Max Length', 'Up to 70 m (single unit)'],
        ['Screw Type', 'Shafted, shaftless, ribbon, paddle'],
        ['Trough Material', 'Carbon steel, stainless steel 304/316'],
      ],
      'faq': [
        ['What is a screw conveyor and how does it work?',
         'A screw conveyor moves powder, granules, and small lumps using a rotating helical screw inside a trough or tube. It is fully enclosed, compact, and ideal for sealed conveying of fine and dusty materials.'],
        ['What materials can a screw conveyor handle?',
         'Cement, fly ash, flour, sugar, starch, sludge, biomass, and chemical powders. Shaftless designs handle sticky and fibrous materials such as wet cake and screenings.'],
        ['What diameters and capacities are available?',
         'Screw diameters range from 100 to 1250 mm, with capacities from 1 to 300 m3/h and single-unit lengths up to 70 m.'],
        ['What is the difference between shafted and shaftless screws?',
         'Shafted screws suit free-flowing dry materials; shaftless screws remove the central shaft to prevent clogging of sticky, fibrous, or wet bulk solids.'],
        ['Is the screw conveyor dust-tight and suitable for hazardous materials?',
         'Yes. The tubular or U-trough design is fully sealed for dust-free operation, and gas-tight versions are available for hazardous or reactive materials.'],
      ],
    },
    'ru': {
      'props': [
        ['Серия моделей', 'LS (стандартный), GX (трубчатый), LC (вертикальный)'],
        ['Диаметр шнека', '100 - 1250 мм'],
        ['Производительность', '1 - 300 м3/ч'],
        ['Макс. длина', 'до 70 м (один агрегат)'],
        ['Тип шнека', 'с валом, безвальный, ленточный, лопастной'],
        ['Материал жёлоба', 'углеродистая сталь, нержавеющая сталь 304/316'],
      ],
      'faq': [
        ['Что такое шнековый конвейер и как он работает?',
         'Шнековый конвейер перемещает порошки, гранулы и мелкие куски с помощью вращающегося винта (шнека) в жёлобе или трубе. Он полностью закрыт, компактен и идеально подходит для герметичной транспортировки мелких и пылящих материалов.'],
        ['Какие материалы может транспортировать шнековый конвейер?',
         'Цемент, летучую золу, муку, сахар, крахмал, осадок сточных вод, биомассу и химические порошки. Безвальные шнеки перемещают липкие и волокнистые материалы, такие как влажный осадок и отсев.'],
        ['Какие диаметры и производительность доступны?',
         'Диаметр шнека - от 100 до 1250 мм, производительность - от 1 до 300 м3/ч, длина одного агрегата - до 70 м.'],
        ['В чём различие между шнеком с валом и безвальным?',
         'Шнеки с валом подходят для сыпучих сухих материалов; безвальные шнеки устраняют центральный вал, предотвращая забивание липких, волокнистых или влажных материалов.'],
        ['Является ли шнековый конвейер пыленепроницаемым и пригоден ли он для опасных сред?',
         'Да. Трубчатая или П-образная конструкция полностью герметична, обеспечивает беспыльную работу, а в герметичном (газонепроницаемом) исполнении подходит для опасных и реакционных материалов.'],
      ],
    },
  },
  'apron-conveyor': {
    'en': {
      'props': [
        ['Model Series', 'BLT (Heavy-Duty Apron Conveyor)'],
        ['Pan Width', '400 - 2400 mm'],
        ['Capacity', 'Up to 1,000 t/h'],
        ['Max Material Temperature', 'Up to 600 deg C'],
        ['Max Inclination', 'Up to 35 deg'],
        ['Pan Material', 'Carbon steel, wear-resistant steel, heat-resistant alloy, stainless steel'],
      ],
      'faq': [
        ['What is an apron conveyor and where is it used?',
         'An apron conveyor uses overlapping steel pans mounted on roller chains to move hot, heavy, and abrasive bulk materials. It is common in steel mills, foundries, cement plants, and mining for clinker, sinter, hot sinter, and scrap.'],
        ['What is the maximum material temperature it can handle?',
         'Standard pans handle moderate temperatures, while heat-resistant alloy steel pans withstand material temperatures up to 600 degrees C.'],
        ['What capacities and inclinations are possible?',
         'Capacities reach up to 1,000 t/h, and inclinations up to 35 degrees depending on material properties.'],
        ['How is an apron conveyor driven?',
         'A low-speed high-torque gear motor is standard; hydraulic drive is optional for soft start and variable speed.'],
        ['How does an apron conveyor compare to a belt conveyor?',
         'Apron conveyors carry hot, heavy, and sharp materials that would damage belts. Belt conveyors are better for cool, fine, high-speed, long-distance transport.'],
      ],
    },
    'ru': {
      'props': [
        ['Серия моделей', 'BLT (тяжёлый пластинчатый конвейер)'],
        ['Ширина полотна', '400 - 2400 мм'],
        ['Производительность', 'до 1 000 т/ч'],
        ['Макс. температура материала', 'до 600°C'],
        ['Макс. угол наклона', 'до 35°'],
        ['Материал полотна', 'углеродистая сталь, износостойкая сталь, жаропрочный сплав, нержавеющая сталь'],
      ],
      'faq': [
        ['Что такое пластинчатый конвейер и где он применяется?',
         'Пластинчатый конвейер использует перекрывающиеся стальные пластины на роликовых цепях для перемещения горячих, тяжёлых и абразивных сыпучих материалов. Применяется на металлургических и литейных заводах, в цементной отрасли и горной промышленности для клинкера, агломерата, горячего спека и металлолома.'],
        ['Какую максимальную температуру материала он выдерживает?',
         'Стандартные пластины выдерживают умеренные температуры, а пластины из жаропрочного сплава - до 600 градусов C.'],
        ['Какие производительность и углы наклона возможны?',
         'Производительность достигает 1 000 т/ч, угол наклона - до 35 градусов в зависимости от свойств материала.'],
        ['Как приводится пластинчатый конвейер?',
         'Стандартно - низкоскоростной высокомоментный редукторный электродвигатель; опционально - гидропривод для плавного пуска и регулировки скорости.'],
        ['Чем пластинчатый конвейер отличается от ленточного?',
         'Пластинчатые конвейеры перемещают горячие, тяжёлые и острые материалы, которые повредили бы ленту. Ленточные конвейеры лучше подходят для холодных, мелких, скоростных перевозок на большие расстояния.'],
      ],
    },
  },
  'dust-collector': {
    'en': {
      'props': [
        ['Model Series', 'PPCS (Pulse-Jet Bag Dust Collector)'],
        ['Air Volume', '5,000 - 500,000 m3/h'],
        ['Filtration Area', '60 - 6,000 m2'],
        ['Dust Emission', '< 30 mg/Nm3'],
        ['Filter Bag Material', 'Polyester, Nomex, PPS, PTFE'],
        ['Operating Temperature', 'Up to 260 deg C'],
      ],
      'faq': [
        ['What is a pulse-jet bag dust collector?',
         'It captures dust from process air using filter bags, with short compressed-air pulses cleaning the bags online or offline. It is widely used in cement, power, metallurgy, chemical, and food plants.'],
        ['What emission level can it achieve?',
         'Outlet dust concentration is below 30 mg/Nm3, meeting strict environmental emission standards.'],
        ['What air volumes and filtration areas are available?',
         'Air volumes range from 5,000 to 500,000 m3/h with filtration areas from 60 to 6,000 m2 to suit small and large plants.'],
        ['What filter bag materials are used?',
         'Polyester for normal temperatures, Nomex and PPS for high temperatures, and PTFE for corrosive or extreme conditions. Operating temperature reaches up to 260 degrees C.'],
        ['Is it suitable for explosive dust?',
         'Yes. Explosion venting, anti-static bags, and spark detection options are available for combustible dust, with ATEX-compliant configurations.'],
      ],
    },
    'ru': {
      'props': [
        ['Серия моделей', 'PPCS (рукавный пылеуловитель с импульсной продувкой)'],
        ['Производительность по воздуху', '5 000 - 500 000 м3/ч'],
        ['Площадь фильтрации', '60 - 6 000 м2'],
        ['Запылённость на выходе', '< 30 мг/нм3'],
        ['Материал рукавов', 'полиэстер, Nomex, PPS, PTFE'],
        ['Рабочая температура', 'до 260°C'],
      ],
      'faq': [
        ['Что такое рукавный пылеуловитель с импульсной продувкой?',
         'Он улавливает пыль из технологического воздуха с помощью фильтровальных рукавов, а короткие импульсы сжатого воздуха очищают рукава на ходу или с остановкой. Широко применяется на цементных, энергетических, металлургических, химических и пищевых предприятиях.'],
        ['Какой уровень выбросов он обеспечивает?',
         'Концентрация пыли на выходе ниже 30 мг/нм3, что соответствует строгим экологическим нормам.'],
        ['Какие производительность по воздуху и площадь фильтрации доступны?',
         'Производительность по воздуху - от 5 000 до 500 000 м3/ч, площадь фильтрации - от 60 до 6 000 м2 для предприятий любого масштаба.'],
        ['Из каких материалов изготавливаются рукава?',
         'Полиэстер для обычных температур, Nomex и PPS для высоких температур, PTFE - для агрессивных и экстремальных условий. Рабочая температура достигает 260 градусов C.'],
        ['Подходит ли он для взрывоопасной пыли?',
         'Да. Доступны взрывные клапаны, антистатические рукава и искроулавливание, а также исполнение по стандарту ATEX.'],
      ],
    },
  },
  'feeding-equipment': {
    'en': {
      'props': [
        ['Types', 'GZG vibrating, GZ electromagnetic vibrating, rotary vane, screw feeder, belt feeder'],
        ['Feed Rate', '5 - 500 t/h'],
        ['Drive', 'Electromagnetic, unbalanced motor, VFD'],
        ['Trough Width', '300 - 1800 mm (vibrating)'],
        ['Body Material', 'Carbon steel, stainless steel'],
        ['Liner', 'Wear-resistant steel, polyurethane, ceramic'],
      ],
      'faq': [
        ['What types of feeding equipment does Tianyi offer?',
         'Vibrating feeders (GZG motor and GZ electromagnetic), rotary vane feeders (airlocks), screw feeders, and belt feeders for controlled material dosing.'],
        ['What is a vibrating feeder used for?',
         'It draws bulk material from a hopper or bin at a steady, controlled rate to a conveyor or crusher, absorbing feed impact and providing even flow.'],
        ['What feed rates are achievable?',
         'Feed rates range from 5 to 500 t/h depending on type and material, with precise adjustment through a variable-frequency drive (VFD).'],
        ['What is a rotary vane feeder and where is it used?',
         'A rotary airlock uses rotating vanes to transfer material between pressurized and unpressurized zones, commonly under dust collectors and for dosing.'],
        ['Are stainless steel and food-grade options available?',
         'Yes. Stainless steel bodies and liners such as polyurethane or ceramic are available for food, chemical, and abrasive applications.'],
      ],
    },
    'ru': {
      'props': [
        ['Типы', 'вибропитатели GZG, электромагнитные вибропитатели GZ, роторные питатели-затворы, шнековые питатели, ленточные питатели'],
        ['Производительность подачи', '5 - 500 т/ч'],
        ['Привод', 'электромагнитный, дебалансный мотор, ПЧ (частотное регулирование)'],
        ['Ширина лотка', '300 - 1800 мм (вибропитатели)'],
        ['Материал корпуса', 'углеродистая сталь, нержавеющая сталь'],
        ['Футеровка', 'износостойкая сталь, полиуретан, керамика'],
      ],
      'faq': [
        ['Какие типы питателей предлагает Тяньи?',
         'Вибрационные питатели (моторные GZG и электромагнитные GZ), роторные питатели-затворы, шнековые и ленточные питатели для дозированной подачи материала.'],
        ['Для чего используется вибрационный питатель?',
         'Он равномерно и с контролируемой скоростью подаёт сыпучий материал из бункера на конвейер или дробилку, гася ударные нагрузки и обеспечивая стабильный поток.'],
        ['Какая производительность подачи достижима?',
         'Производительность составляет от 5 до 500 т/ч в зависимости от типа и материала, с точной настройкой через преобразователь частоты (ПЧ).'],
        ['Что такое роторный питатель-затвор и где он применяется?',
         'Роторный затвор-блокиратор переносит материал между зонами с разным давлением с помощью вращающихся лопастей, обычно устанавливается под пылеуловителями и для дозирования.'],
        ['Доступны ли нержавеющие и пищевые исполнения?',
         'Да. Корпуса из нержавеющей стали и футеровки из полиуретана или керамики доступны для пищевой, химической и абразивной сред.'],
      ],
    },
  },
  'crushing-equipment': {
    'en': {
      'props': [
        ['Types', 'Jaw (PE), Hammer (PC), Roll (2PG), Impact'],
        ['Max Feed Size', 'Up to 1,200 mm'],
        ['Output Size', '5 - 150 mm'],
        ['Capacity', '5 - 1,000 t/h'],
        ['Crushing Ratio', '4:1 to 20:1'],
        ['Wear Parts', 'Manganese steel (Mn13/Mn18), high-chrome alloy'],
      ],
      'faq': [
        ['What crusher types are available?',
         'Jaw crushers (PE) for primary crushing, hammer crushers (PC) for medium-hard brittle materials, roll crushers (2PG) for sticky or soft materials, and impact crushers for cubic products.'],
        ['What is the maximum feed size and output size?',
         'Maximum feed size reaches 1,200 mm, and the output size is adjustable from 5 to 150 mm.'],
        ['What capacities are possible?',
         'Capacities range from 5 to 1,000 t/h depending on model and material, with crushing ratios from 4:1 to 20:1.'],
        ['How is the discharge size adjusted?',
         'By manual wedge, hydraulic, or shim adjustment to control the product grading.'],
        ['What wear parts are used?',
         'Manganese steel (Mn13/Mn18) for jaws and rolls, and high-chrome alloy for hammers, ensuring long service life under abrasion.'],
      ],
    },
    'ru': {
      'props': [
        ['Типы', 'щёковые (PE), молотковые (PC), валковые (2PG), роторные'],
        ['Макс. размер загрузки', 'до 1 200 мм'],
        ['Размер продукта', '5 - 150 мм'],
        ['Производительность', '5 - 1 000 т/ч'],
        ['Степень дробления', 'от 4:1 до 20:1'],
        ['Изнашиваемые части', 'сталь Г13/Г18 (марганцовистая), высокохромистый сплав'],
      ],
      'faq': [
        ['Какие типы дробилок доступны?',
         'Щёковые дробилки (PE) для первичного дробления, молотковые (PC) для среднетвёрдых хрупких материалов, валковые (2PG) для липких и мягких материалов, роторные - для кубовидного продукта.'],
        ['Каков максимальный размер загрузки и продукта?',
         'Максимальный размер загрузки достигает 1 200 мм, размер продукта регулируется от 5 до 150 мм.'],
        ['Какая производительность возможна?',
         'Производительность составляет от 5 до 1 000 т/ч в зависимости от модели и материала, степень дробления - от 4:1 до 20:1.'],
        ['Как регулируется размер продукта?',
         'С помощью ручного клинового, гидравлического или прокладочного механизма для управления гранулометрией.'],
        ['Из чего изготавливаются изнашиваемые части?',
         'Марганцовистая сталь (Г13/Г18) для щёк и валков, высокохромистый сплав для молотков - для длительного срока службы при абразивном износе.'],
      ],
    },
  },
  'screening-equipment': {
    'en': {
      'props': [
        ['Types', 'Linear vibrating (ZK), circular vibrating (YA)'],
        ['Screen Size', '1200x2400 to 3000x7200 mm'],
        ['Decks', '1 - 4'],
        ['Capacity', '10 - 800 t/h'],
        ['Mesh Size', '3 - 150 mm'],
        ['Material', 'Carbon steel, stainless steel'],
      ],
      'faq': [
        ['What screen types are offered?',
         'Linear vibrating screens (ZK series) and circular vibrating screens (YA series), configurable with 1 to 4 decks for multi-size classification.'],
        ['What sizes and capacities are available?',
         'Screen areas range from 1200x2400 to 3000x7200 mm, with capacities from 10 to 800 t/h and mesh sizes from 3 to 150 mm.'],
        ['How many decks can be configured?',
         'Up to 4 decks allow separation into multiple size fractions in a single pass.'],
        ['What motion types are used?',
         'Circular, linear, or elliptical vibration selected to suit the material and screening duty.'],
        ['Are stainless steel screens available for food and chemical use?',
         'Yes. Stainless steel construction is offered for food, chemical, and corrosive applications.'],
      ],
    },
    'ru': {
      'props': [
        ['Типы', 'линейные вибрационные (ZK), гирационные вибрационные (YA)'],
        ['Размер просеивателя', '1200x2400 - 3000x7200 мм'],
        ['Число ярусов', '1 - 4'],
        ['Производительность', '10 - 800 т/ч'],
        ['Размер ячейки', '3 - 150 мм'],
        ['Материал', 'углеродистая сталь, нержавеющая сталь'],
      ],
      'faq': [
        ['Какие типы грохотов предлагаются?',
         'Линейные вибрационные грохоты (серия ZK) и гирационные вибрационные грохоты (серия YA) с 1-4 ярусами для разделения на несколько фракций.'],
        ['Какие размеры и производительность доступны?',
         'Площадь просеивания - от 1200x2400 до 3000x7200 мм, производительность - от 10 до 800 т/ч, размер ячейки - от 3 до 150 мм.'],
        ['Сколько ярусов можно установить?',
         'До 4 ярусов позволяет разделять материал на несколько фракций за один проход.'],
        ['Какой тип вибрации используется?',
         'Круговая, линейная или эллиптическая вибрация подбирается под материал и задачу грохочения.'],
        ['Доступны ли грохоты из нержавеющей стали для пищевой и химической отрасли?',
         'Да. Исполнение из нержавеющей стали предлагается для пищевых, химических и агрессивных сред.'],
      ],
    },
  },
  'valves': {
    'en': {
      'props': [
        ['Types', 'Plug-in, flap, roller gate, three-way, four-way, E-type gate'],
        ['Size Range', 'DN150 - DN1000'],
        ['Material', 'Carbon steel, stainless steel'],
        ['Actuation', 'Manual, electric, pneumatic, hydraulic'],
        ['Working Pressure', 'Up to 1.6 MPa'],
        ['Explosion-Proof', 'ATEX/IECEx compliant actuators'],
      ],
      'faq': [
        ['What industrial valves does Tianyi supply?',
         'Plug-in valves, flap valves, roller gates, three-way valves, four-way valves, and E-type gate valves for bulk material handling lines.'],
        ['What sizes and actuation options are available?',
         'Sizes range from DN150 to DN1000, with manual handwheel, electric motor, pneumatic cylinder, or hydraulic actuation.'],
        ['What sealing options are offered?',
         'Metal-to-metal, soft seals (EPDM/NBR/PTFE), and inflatable seals for dust-tight shutoff.'],
        ['Are explosion-proof versions available?',
         'Yes. Pneumatic and electric actuators can be supplied with ATEX/IECEx compliance for combustible dust environments.'],
        ['How are the valves controlled?',
         'Via local push-button, remote PLC/DCS, with position feedback sensors and limit switches for automation.'],
      ],
    },
    'ru': {
      'props': [
        ['Типы', 'шиберные, поворотные (хлопушки), роликовые задвижки, трёхходовые, четырёхходовые, Е-образные шиберы'],
        ['Типоразмер', 'DN150 - DN1000'],
        ['Материал', 'углеродистая сталь, нержавеющая сталь'],
        ['Привод', 'ручной, электрический, пневматический, гидравлический'],
        ['Рабочее давление', 'до 1,6 МПа'],
        ['Взрывозащита', 'приводы по ATEX/IECEx'],
      ],
      'faq': [
        ['Какие промышленные затворы и клапаны поставляет Тяньи?',
         'Шиберные задвижки, поворотные затворы (хлопушки), роликовые задвижки, трёх- и четырёхходовые клапаны, Е-образные шиберы для линий транспортировки сыпучих материалов.'],
        ['Какие типоразмеры и приводы доступны?',
         'Типоразмер от DN150 до DN1000 с ручным маховиком, электрическим, пневматическим или гидравлическим приводом.'],
        ['Какие варианты уплотнения предлагаются?',
         'Металл по металлу, мягкое уплотнение (EPDM/NBR/PTFE) и надувное уплотнение для герметичного перекрытия.'],
        ['Доступны ли взрывозащищённые исполнения?',
         'Да. Пневматические и электрические приводы могут поставляться во взрывозащищённом исполнении по ATEX/IECEx для сред с горючей пылью.'],
        ['Как управляются затворы?',
         'С помощью местной кнопки, удалённого ПЛК/АСУ ТП, с датчиками положения и конечными выключателями для автоматизации.'],
      ],
    },
  },
  'parts': {
    'en': {
      'props': [
        ['Categories', 'Idlers, sprockets and chains, buckets, bearings and couplings, wear liners'],
        ['Sprocket Pitch', '50.8 - 304.8 mm'],
        ['Bucket Capacity', '0.5 - 80 L'],
        ['Bucket Material', 'Plastic, carbon steel, stainless steel, wear-resistant alloy'],
        ['Wear Liners', 'Ceramic, bi-metallic, polyurethane, Hardox, chromium carbide'],
        ['Lead Time', '3-5 days (standard), 2-4 weeks (custom)'],
      ],
      'faq': [
        ['What spare parts does Tianyi supply?',
         'Conveyor idlers, sprockets and chains, buckets, bearings and couplings, and wear liners for bulk handling systems.'],
        ['What idler and bucket types are available?',
         'Trough, flat, impact, and self-aligning idlers; belt and chain buckets in plastic, steel, and wear-resistant alloy with capacities from 0.5 to 80 L.'],
        ['What chain and sprocket specifications are offered?',
         'Drive and roller chains, drop-forged scraper chains, and pintle or welded bucket elevator chains, with sprocket pitches from 50.8 to 304.8 mm.'],
        ['What wear liner materials are used?',
         'Ceramic (alumina), bi-metallic, polyurethane, Hardox, and chromium carbide overlay for extended service life.'],
        ['What are the typical lead times?',
         'Standard parts ship in 3-5 days; custom-fabricated parts take 2-4 weeks.'],
      ],
    },
    'ru': {
      'props': [
        ['Категории', 'ролики, звёздочки и цепи, ковши, подшипники и муфты, футеровки'],
        ['Шаг звёздочки', '50,8 - 304,8 мм'],
        ['Вместимость ковша', '0,5 - 80 л'],
        ['Материал ковша', 'пластик, углеродистая сталь, нержавеющая сталь, износостойкий сплав'],
        ['Футеровка', 'керамика, биметалл, полиуретан, Hardox, наплавка карбидом хрома'],
        ['Срок поставки', '3-5 дней (стандарт), 2-4 недели (на заказ)'],
      ],
      'faq': [
        ['Какие запасные части поставляет Тяньи?',
         'Ролики конвейеров, звёздочки и цепи, ковши, подшипники и муфты, а также футеровки для систем транспортировки сыпучих материалов.'],
        ['Какие типы роликов и ковшей доступны?',
         'Желобчатые, плоские, амортизирующие и самоцентрирующиеся ролики; ковши ленточных и цепных элеваторов из пластика, стали и износостойкого сплава вместимостью 0,5-80 л.'],
        ['Какие цепи и звёздочки предлагаются?',
         'Приводные и роликовые цепи, кованые скребковые цепи, а также штыревые и сварные цепи ковшовых элеваторов с шагом звёздочки 50,8-304,8 мм.'],
        ['Из каких материалов изготавливается футеровка?',
         'Керамика (оксид алюминия), биметалл, полиуретан, Hardox и наплавка карбидом хрома для продления срока службы.'],
        ['Какие типичные сроки поставки?',
         'Стандартные детали - 3-5 дней; детали по индивидуальному заказу - 2-4 недели.'],
      ],
    },
  },
  'chain-conveyor': {
    'ru': {
      'props': [
        ['Серия моделей', 'MS (горизонтальный), MC (наклонный), MZ (вертикальный / Z-образный)'],
        ['Ширина корпуса', '160 - 1000 мм'],
        ['Производительность', '6 - 500 т/ч'],
        ['Макс. длина', 'до 80 м'],
        ['Макс. высота подъёма', 'до 40 м'],
        ['Тип цепи', 'сварная круглозвенная, кованая, литая'],
      ],
      'faq': [
        ['Что такое цепной конвейер en-masse и как он работает?',
         'Цепной конвейер en-masse (скребковый или тяговый) перемещает сыпучий материал внутри полностью закрытого прямоугольного корпуса с помощью непрерывной цепи со скребками. Скребки проталкивают материал сплошным столбом, обеспечивая горизонтальную, наклонную и даже вертикальную транспортировку с минимальным пылением.'],
        ['Какие материалы может транспортировать цепной конвейер Тяньи?',
         'Абразивные и высокотемпературные сыпучие материалы: уголь, золу, клинкер, цемент, кальцинированную соду, зерно, биомассу, древесную щепу и химические порошки. Для тяжёлых условий предусмотрены износостойкие футеровки и термостойкие цепи.'],
        ['В чём различие между цепными конвейерами MS, MC и MZ?',
         'MS - горизонтальный тип, MC - наклонный, MZ - вертикальный / Z-образный (en-masse). Все они используют закрытый корпус, но отличаются компоновкой для горизонтальных, наклонных или вертикальных трасс.'],
        ['Какова максимальная производительность и длина транспортировки?',
         'Производительность - от 6 до 500 т/ч в зависимости от материала и корпуса. Максимальная горизонтальная длина - около 80 м, вертикальный подъём - до 40 м; большие значения достигаются каскадом агрегатов.'],
        ['Является ли цепной конвейер пыленепроницаемым и пригодным для взрывоопасной пыли?',
         'Да. Корпус полностью герметичен. Для горючей пыли (зерно, мука, древесные отходы) предусмотрены взрывозащищённые исполнения с разрывными мембранами и антистатическими элементами.'],
      ],
    },
  },
  'bucket-elevator': {
    'ru': {
      'props': [
        ['Серия моделей', 'TH (глубокий ковш), TD (ленточный), NE (цепной)'],
        ['Производительность', '4 - 800 м3/ч'],
        ['Высота подъёма', 'до 60 м'],
        ['Ширина ковша', '160 - 800 мм'],
        ['Тип привода', 'ленточный (TD), цепной (TH, NE)'],
        ['Материал ковша', 'углеродистая сталь, нержавеющая сталь, износостойкая сталь, HDPE'],
      ],
      'faq': [
        ['Что такое ковшовый элеватор и для чего он используется?',
         'Ковшовый элеватор вертикально перемещает сыпучие материалы (зерно, цемент, уголь, минералы) с помощью ковшей, закреплённых на ленте или цепи. Применяется на элеваторах, в цементной, горной и химической отраслях.'],
        ['В чём различие между сериями TH, TD и NE?',
         'TD - ленточный элеватор для средних нагрузок; TH - цепной с глубокими ковшами для высокой производительности; NE - тяжёлый цепной элеватор для абразивных и крупных материалов.'],
        ['Какую максимальную производительность и высоту обеспечивает элеватор?',
         'Производительность достигает 800 м3/ч, высота подъёма - до 60 м, при индивидуальном проектировании - выше.'],
        ['Является ли элеватор взрывозащищённым для зерна и пыли?',
         'Да. Корпус оснащается взрывозащитными клапанами, датчиками схода ленты и переполнения, а для зерновых предусмотрено антистатическое исполнение.'],
        ['Какие материалы ковшей используются?',
         'Углеродистая и нержавеющая сталь, износостойкая сталь и пищевой пластик HDPE для зерна; выбор зависит от материала и условий эксплуатации.'],
      ],
    },
  },
}


def build_faq_html(faq, title):
    items = "\n".join(
        f'      <div class="faq-item">\n        <h3>{q}</h3>\n        <p>{a}</p>\n      </div>' for q, a in faq
    )
    return (
        '<section class="section" id="faq">\n'
        '  <div class="container">\n'
        f'    <h2>{title}</h2>\n'
        '    <div class="faq-list">\n'
        f'{items}\n'
        '    </div>\n'
        '  </div>\n'
        '</section>'
    )


def process(path, lang, props, faq):
    raw = path.read_text(encoding='utf-8')
    orig = raw
    title = 'Frequently Asked Questions' if lang == 'en' else 'Часто задаваемые вопросы'

    # 1. FAQ HTML section before CTA
    if 'id="faq"' not in raw:
        assert CTA_ANCHOR in raw, f"CTA anchor missing in {path}"
        faq_html = build_faq_html(faq, title)
        raw = raw.replace(CTA_ANCHOR, faq_html + "\n\n" + CTA_ANCHOR, 1)

    # 2. FAQ CSS
    if '/* FAQ (GEO template) */' not in raw:
        assert CSS_ANCHOR in raw, f"CSS anchor missing in {path}"
        raw = raw.replace(CSS_ANCHOR, CSS_ANCHOR + FAQ_CSS, 1)

    # 3. Product schema (additionalProperty) + FAQPage
    m = re.search(r'<script type="application/ld\+json">(.*?)</script>', raw, re.S)
    if m:
        data = json.loads(m.group(1))
        if data.get('@type') == 'Product':
            if 'additionalProperty' not in data:
                data['additionalProperty'] = [
                    {"@type": "PropertyValue", "name": n, "value": v} for n, v in props
                ]
            product_script = (
                '<script type="application/ld+json">\n'
                + json.dumps(data, indent=2, ensure_ascii=False)
                + '\n</script>'
            )
            if 'FAQPage' not in raw:
                faqpage = {
                    "@context": "https://schema.org",
                    "@type": "FAQPage",
                    "mainEntity": [
                        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
                        for q, a in faq
                    ],
                }
                faqpage_script = (
                    '<script type="application/ld+json">\n'
                    + json.dumps(faqpage, indent=2, ensure_ascii=False)
                    + '\n</script>'
                )
                replacement = product_script + "\n\n" + faqpage_script
            else:
                replacement = product_script
            raw = raw[: m.start()] + replacement + raw[m.end():]

    if raw != orig:
        path.write_text(raw, encoding='utf-8')
        print(f"UPDATED {path}")
    else:
        print(f"NOCHANGE {path}")


def validate(path, faq):
    raw = path.read_text(encoding='utf-8')
    blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', raw, re.S)
    faq_count = 0
    product_ok = False
    for b in blocks:
        d = json.loads(b)
        if d.get('@type') == 'Product':
            product_ok = 'additionalProperty' in d
        elif d.get('@type') == 'FAQPage':
            qa = d.get('mainEntity', [])
            faq_count = len(qa)
            for item in qa:
                q = item['name']
                a = item['acceptedAnswer']['text']
                assert q in raw, f"FAQ Q not in HTML: {q[:40]}"
                assert a in raw, f"FAQ A not in HTML: {a[:40]}"
    visible = len(re.findall(r'class="faq-item"', raw))
    assert product_ok, "Product additionalProperty missing"
    assert faq_count == len(faq), f"FAQ count {faq_count} != {len(faq)}"
    assert visible == faq_count, f"visible {visible} != schema {faq_count}"
    assert 'id="faq"' in raw
    print(f"VALID   {path}  (faq={faq_count}, visible={visible})")


print("=== APPLY ===")
for slug, cfg in CONFIG.items():
    for lang in ('en', 'ru'):
        if lang not in cfg:
            continue
        sub = 'products' if lang == 'en' else 'ru/products'
        path = BASE / sub / f'{slug}.html'
        process(path, lang, cfg[lang]['props'], cfg[lang]['faq'])

print("\n=== VALIDATE ===")
for slug, cfg in CONFIG.items():
    for lang in ('en', 'ru'):
        if lang not in cfg:
            continue
        sub = 'products' if lang == 'en' else 'ru/products'
        path = BASE / sub / f'{slug}.html'
        validate(path, cfg[lang]['faq'])

print("\nDONE")

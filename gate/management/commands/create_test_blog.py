from django.core.management.base import BaseCommand
from comments.models import Comments
from catalog.models import Catalog
from blog.models import Blog
from user.models import User


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        catalog_main = Catalog(name="/", title="Главная")
        catalog_main.save()
        catalog1 = Catalog(name="cat1", title="каталог 1", parent=catalog_main)
        catalog1.save()
        blog1 = Blog(
            name="blog1",
            title="Блог 1",
            text="""<h3>Опыт Ву</h3>
            <p>
            Опыт Ву — эксперимент в области физики элементарных частиц и ядерной физики, проведённый в 1956 году китайским и американским физиком Цзяньсюн Ву в сотрудничестве с Лабораторией низких температур Национального бюро стандартов США[1][2]. Целью опыта было установить, сохраняется ли чётность (P-чётность[3]), которая ранее была установлена в электромагнитных и сильных взаимодействиях, также для слабого взаимодействия или нет. Если P-чётность была бы истинной сохраняющейся величиной, то зеркальная версия мира (где левое заменяется на правое, а правое — на левое) вела бы себя как зеркальное отображение настоящего мира. Если P-чётность была бы нарушена, то можно было бы различать зеркальную версию мира и зеркальное отображение настоящего мира. Опыт состоял в наблюдении распределения направлений вылета электронов из ядер кобальта-60 при бета-распаде в условиях очень низкой температуры и сильного магнитного поля. В нём обнаружилась асимметрия распределения бета-частиц, вылетающих из источника радиации.
            Результаты опыта показали, что сохранение пространственной чётности нарушается из-за слабого взаимодействия, что приводит к возможности оперативно определять левое и правое[en] без привязки к макрообъектам реального мира. Этот результат не был ожидаемым в физическом сообществе, которое раньше считало чётность сохраняющейся величиной[en]. Чжэндао Ли и Чжэньнин Янг, физики-теоретики, которые положили начало идее несохранения чётности и предложили этот эксперимент, получили за свою теоретическую работу Нобелевскую премию по физике 1957 года. Роль Ву Цзяньсюн в открытии была упомянута в нобелевской речи[4], но не была отмечена вплоть до 1978 года, когда ей впервые присудили премию Вольфа.
            </p>
            <h3>История</h3>
            <p>
            В 1927 году Юджин Вигнер формализовал принцип сохранения чётности (P-чётности)[5] — идею о том, что настоящий мир и мир, построенный как его зеркальное отображение, будут вести себя одинаково, с той лишь разницей, что левое и правое будут перевёрнуты (например, часы, которые идут по часовой стрелке, будут вращаться против часовой стрелки, в зеркальном мире).
            Этот принцип был широко принят физиками, а сохранение P-чётности экспериментально подтвердили в электромагнитных и сильных взаимодействиях. Однако в середине 1950-х годах некоторые распады с участием каонов не могли быть объяснены существующими теориями, в которых предполагалось, что P-чётность сохраняется. Казалось, что существует два типа каонов: один распадается на два пиона, а другой — на три пиона. Этот эффект получил название τ — θ-парадокс[6][7].
            Чжэндао Ли и Чжэньнин Янг положили начало идее несохранения чётности. Они провели обзор литературы по вопросу сохранения чётности во всех фундаментальных взаимодействиях и пришли к выводу, что в случае слабого взаимодействия экспериментальные данные не подтверждают и не опровергают наличия P-симметрии[8][9]. Вскоре после этого они обратились к Цзяньсюн Ву, эксперту по спектроскопии бета-распада, с различными идеями для экспериментов. Они остановились на идее проверить направленность бета-распада в кобальте-60. Ву осознала потенциал революционного эксперимента и, желая опередить остальное физическое сообщество, приступила к работе в конце мая 1956 года, отменив запланированную поездку в Женеву и на Дальний Восток со своим мужем. Большинство физиков, включая её близкого друга Вольфганга Паули, считали это невозможным[10]. Другой известный учёный, Ричард Фейнман, заключил пари 10 000 к 1 с физиком Норманом Рамзеем на провал эксперимента; узнав о его результатах, он договорился на пятьдесят долларов — сумму, которую он позже заплатит Рамзею на Рочестерской конференции[11][12].
            Ву пришлось связаться с Генри Бурсом и Марком Земанским[en], которые имели большой опыт в физике низких температур, чтобы провести свой эксперимент. По просьбе Бурса и Земанского Ву связалась с Эрнестом Амблером[en] из Национального бюро стандартов для помощи в организации эксперимента, который должен был состояться в 1956 году в Лаборатории низких температур Национального бюро стандартов[6]. В декабре 1956 года после нескольких месяцев работы и преодоления технических трудностей команда Ву установила асимметрию, указывающую на нарушение чётности[13].
            Ли и Янг, которые инициировали опыт Ву, за свою теоретическую работу были награждены Нобелевской премией по физике в 1957 году, вскоре после проведения эксперимента. Роль Ву в открытии была упомянута в речи во время вручения премии[4]. Вольфганг Паули, Янг, Ли и многие другие учёные были возмущены таким решением Нобелевского комитета, а лауреат Нобелевской премии 1988 года Джек Штайнбергер назвал это самой большой ошибкой в истории Нобелевского комитета[14]. В 1978 году Ву была присуждена первая премия Вольфа[15].
            </p>""",
            catalog=catalog1,
        )
        blog1.save()
        blog2 = Blog(
            name="blog2",
            title="Блог 2",
            text="""
            <h3>Павел Филиппович Горпищенко</h3>
            <p>Павел Филиппович Горпищенко (13 декабря 1893 — 28 ноября 1943) — советский военный деятель, полковник, участник Первой мировой, Гражданской и Великой Отечественной войн. В межвоенные годы — командир ряда батарей береговой обороны Черноморского флота. В годы Великой Отечественной войны — командир 1-го Севастопольского полка морской пехоты, 8-й бригады морской пехоты и 77-й Симферопольской Краснознамённой стрелковой дивизии.</p>
            <h3>Первая мировая и гражданская война</h3>
            <p>
            Родился 13 декабря 1893 года в станице Пашковской Кубанской области (нынешний Краснодарский край). Мобилизован на военную службу в Первую мировую войну в 1914 году, службу проходил как рядовой Карской крепостной артиллерии на Кавказском фронте. С 1917 года служил в Эрзерумском артиллерийском полку[1].
            С 1918 года участвовал в Гражданской войне на стороне красноармейцев как доброволец. Член ВКП(б) с 1919 года[1]. Командир отделения позиционной батареи в Новороссийске (май 1920 года), с июля 1920 года командовал 2-й полевой тяжёлой батареей 9-й армии, в феврале 1921 года назначен на аналогичную должность в 1-й полевой тяжёлой батареи. С августа 1921 года — исполняющий должность инструктора для поручений при артиллерийском отделе Кавказского сектора, с октября 1921 года — командир 3-й и 1-й батарей[1].
            </p>
            <h3>Межвоенные годы</h3>
            <p>
            Продолжил службу в береговой артиллерии после войны. С октября 1923 года — командир батареи берегового дивизиона Новороссийской группы. С февраля 1924 года — командир батареи 2-го дивизиона Севастопольской крепости. С ноября 1926 года — командир батареи Батумского укрепрайона. C февраля 1928 года занимал должность помощника командира дивизиона 6‑й крепостной артиллерийской бригады. В июле 1930 года назначен помощником начальника сектора Технического управления Управления ВМС СССР. С февраля 1932 года — командир башни № 7 1‑й бригады береговой обороны Морских сил Балтийского моря. С мая 1932 года командовал железнодорожной батареей Ижорского укрепрайона. В октябре 1934 года переведен в 4‑е училище береговой обороны (Севастопольское военно-морское училище имени ЛКСМУ), где преподавал и занимал должность командира 4‑го дивизиона. С февраля 1938 года — начальник школы оружия учебного отряда Черноморского флота[1].
            </p>
            """,
            catalog=catalog1,
        )
        blog2.save()
        comment1 = Comments(
            text="просто комментарий",
            owner=blog1,
        )
        comment1.save()
        comment2 = Comments(
            text="ответ на комментарий",
            parent=comment1,
        )
        comment2.save()
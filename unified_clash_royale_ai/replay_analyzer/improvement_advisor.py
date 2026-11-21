from .error_analyzer import ErrorAnalyzer
class ImprovementAdvisor :
    def __init__ (self ):
        self .error_analyzer =ErrorAnalyzer ()
    def analyze_and_advise (self ,replay ):
        errors =self .error_analyzer .analyze_replay (replay )
        error_summary =self .error_analyzer .get_error_summary (errors )
        recommendations =self ._generate_recommendations (errors ,error_summary )
        priorities =self ._prioritize_recommendations (recommendations )
        return {
        'errors':errors ,
        'summary':error_summary ,
        'recommendations':recommendations ,
        'priorities':priorities ,
        'overall_score':self ._calculate_score (errors )
        }
    def _generate_recommendations (self ,errors ,summary ):
        recommendations =[]
        if summary ['by_type'].get ('elixir_leak',0 )>2 :
            recommendations .append ({
            'category':'Управление эликсиром',
            'title':'Уменьшите утечку эликсира',
            'description':'Вы часто достигаете 10 эликсира без действий. '
            'Старайтесь играть карты до достижения максимума.',
            'exercises':[
            'Следите за счетчиком эликсира',
            'Планируйте ходы заранее',
            'Используйте дешевые карты для цикла'
            ],
            'priority':'high'
            })
        if summary ['by_type'].get ('bad_placement',0 )>2 :
            recommendations .append ({
            'category':'Размещение карт',
            'title':'Улучшите позиционирование',
            'description':'Ваше размещение карт не всегда оптимально.',
            'exercises':[
            'Изучите оптимальные позиции для каждой карты',
            'Размещайте танков сзади',
            'Здания ставьте в центр для оттягивания'
            ],
            'priority':'medium'
            })
        if summary ['by_type'].get ('early_aggression',0 )>0 :
            recommendations .append ({
            'category':'Тайминг',
            'title':'Будьте терпеливее в начале',
            'description':'Вы атакуете слишком рано, не накопив преимущество.',
            'exercises':[
            'Ждите 10 эликсира перед первой атакой',
            'Пусть противник сделает первый ход',
            'Играйте реактивно в начале матча'
            ],
            'priority':'high'
            })
        if summary ['by_type'].get ('wrong_card',0 )>2 :
            recommendations .append ({
            'category':'Выбор карт',
            'title':'Изучите контрпики',
            'description':'Вы не всегда выбираете правильную карту для ситуации.',
            'exercises':[
            'Изучите таблицу контрпиков',
            'Следите за картами противника',
            'Запоминайте ротацию противника'
            ],
            'priority':'medium'
            })
        if not recommendations :
            recommendations .append ({
            'category':'Общее',
            'title':'Хорошая игра!',
            'description':'Серьезных ошибок не обнаружено. Продолжайте практиковаться.',
            'exercises':[
            'Работайте над микроменеджментом',
            'Изучайте новые колоды',
            'Смотрите профессиональные матчи'
            ],
            'priority':'low'
            })
        return recommendations
    def _prioritize_recommendations (self ,recommendations ):
        priority_order ={'high':0 ,'medium':1 ,'low':2 }
        sorted_recs =sorted (
        recommendations ,
        key =lambda x :priority_order .get (x .get ('priority','low'),2 )
        )
        return [rec ['title']for rec in sorted_recs [:3 ]]
    def _calculate_score (self ,errors ):
        base_score =100
        severity_penalties ={
        'high':15 ,
        'medium':8 ,
        'low':3
        }
        for error in errors :
            severity =error .get ('severity','low')
            base_score -=severity_penalties .get (severity ,3 )
        return max (0 ,min (100 ,base_score ))
    def generate_report (self ,replay ):
        analysis =self .analyze_and_advise (replay )
        report =[]
        report .append ("="*60 )
        report .append ("📊 ОТЧЕТ ПО МАТЧУ")
        report .append ("="*60 )
        report .append ("")
        result_emoji ={'win':'🏆','loss':'❌','draw':'🤝'}.get (
        replay .result ,'❓'
        )
        report .append (f"Результат: {result_emoji } {replay .result or 'Неизвестно'}")
        report .append (f"Оценка: {analysis ['overall_score']}/100")
        report .append ("")
        report .append ("📉 ОШИБКИ")
        report .append ("-"*40 )
        summary =analysis ['summary']
        report .append (f"Всего ошибок: {summary ['total_errors']}")
        report .append (f"  Критических: {summary ['by_severity']['high']}")
        report .append (f"  Средних: {summary ['by_severity']['medium']}")
        report .append (f"  Незначительных: {summary ['by_severity']['low']}")
        report .append ("")
        report .append ("💡 РЕКОМЕНДАЦИИ")
        report .append ("-"*40 )
        for rec in analysis ['recommendations']:
            report .append (f"\n{rec ['category']}: {rec ['title']}")
            report .append (f"  {rec ['description']}")
            report .append ("  Упражнения:")
            for ex in rec ['exercises']:
                report .append (f"    • {ex }")
        report .append ("")
        report .append ("="*60 )
        return "\n".join (report )
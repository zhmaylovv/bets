from app.models import User, Match, Bets
from app import db


def result_calc (match_id, ):
    """
    Перерасчет всех результатов
        :param match_list:
                            match_list = {'game_id_here': {'result': [0, 0],
                                                         'bets': {'player0': [0, 0],
                                                                'player1': [0, 0],
                                                                'player2': [0, 0],
                                                                'player3': [0, 0]
                                                                }

                                                         }
                      }

    :return: score_dict
    """
    score_dict = []
    match= Match.query.filter_by(id=match_id).first_or_404()
    users = User.query.all()
    bets = Bets.query.all()

    for bet in bets:
        bet.res_scor = 0
        try:
            bet1 = bet.t1_pre
            bet2 = bet.t2_pre
        except:
            bet1 = 0
            bet2 = 0

        res1 = match.t1_res
        res2 = match.t2_res

        if res1 == res2:  # если ничья, 4 очка
            if bet1 == res1 and bet2 == res2:
                bet.res_scor += 4
            elif bet1 == bet2:
                bet.res_scor += 3
        elif bet1 == res1 and bet2 == res2:  # 5 очков
            bet.res_scor += 5
        elif res1 > res2 and bet1 > bet2:
            if res1 - res2 == bet1 - bet2:
                bet.res_scor += 3
            else:
                bet.res_scor += 2
        elif res1 < res2 and bet1 < bet2:
            if res1 - res2 == bet1 - bet2:
                bet.res_scor += 3
            else:
                bet.res_scor += 2


        db.session.commit ()
    pass


from app.models import User, Match, Bets



def result_calc ():
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
    matchs = Match.query.all()
    bets = Bets.query.all()

    for bet in bets:
        bet.res_score = 0
        bet1 = bet.t1_pre
        bet2 = bet.t2_pre
        res1 = Match.query.filter_by(id=bet.match_id).first_or_404().t1_res
        res2 = Match.query.filter_by(id=bet.match_id).first_or_404().t2_res

        if res1 == res2:  # если ничья, 4 очка
            if bet1 == res1 and bet2 == res2:
                bet.res_score += 4
            elif bet1 == bet2:
                bet.res_score += 3
        elif bet1 == res1 and bet2 == res2:  # 5 очков
            bet.res_score += 5
        elif res1 > res2 and bet1 > bet2:
            if res1 - res2 == bet1 - bet2:
                bet.res_score += 3
            else:
                bet.res_score += 2
        elif res1 < res2 and bet1 < bet2:
            if res1 - res2 == bet1 - bet2:
                bet.res_score += 3
            else:
                bet.res_score += 2

        """
        print ( "user:" ,bet.user_id ,"match:" ,bet.match_id ,"bet:" ,bet1 ,bet2 ,"res:" ,res1 ,res2 ,"score:" ,
                bet.res_score )
        
        user: 2 match: 1 bet: 123 123 res: 1 0 score: 0
        user: 2 match: 2 bet: 2 0 res: 2 0 score: 5
        user: 2 match: 3 bet: 3 0 res: 5 0 score: 2
        user: 3 match: 1 bet: 4 4 res: 1 0 score: 0
        user: 3 match: 2 bet: 5 5 res: 2 0 score: 0
        user: 3 match: 3 bet: 6 6 res: 5 0 score: 0
        user: 4 match: 1 bet: 5 5 res: 1 0 score: 0
        user: 4 match: 4 bet: 3 3 res: 5 5 score: 3
        user: 5 match: 1 bet: 10 5 res: 1 0 score: 2
        user: 5 match: 2 bet: 5 5 res: 2 0 score: 0
        user: 5 match: 3 bet: 4 4 res: 5 0 score: 0
        user: 6 match: 3 bet: 1 2 res: 5 0 score: 0

        """
    pass

    '''for j in match_list[i]["bets"]:
                res1, res2 = int(match_list[i]["result"][0]), int(match_list[i]["result"][1])
                bet1, bet2 = int(match_list[i]["bets"][j][0]), int(match_list[i]["bets"][j][1])
                if j not in score_dict:
                    bet.res_score = 0'''
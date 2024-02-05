import ast
import uuid
import warnings
warnings.filterwarnings('ignore')
# setup disply parameters
import matplotlib
matplotlib.use('Agg')

from negmas import (
    make_issue,
    SAOMechanism,
    NaiveTitForTatNegotiator,
    TimeBasedConcedingNegotiator,
)
from negmas.preferences import LinearAdditiveUtilityFunction as LUFun
from negmas.preferences.value_fun import LinearFun, IdentityFun, AffineFun


def get_issues():
    # create negotiation agenda (issues)
    issues = [
        make_issue(name="price", values=10),
        make_issue(name="quantity", values=(1, 11)),
        make_issue(name="delivery_time", values=10),
    ]
    return issues


def process(n_steps):
    # create the mechanism
    session = SAOMechanism(issues=get_issues(), n_steps=n_steps)

    # define buyer and seller utilities
    seller_utility = LUFun(
        values=[IdentityFun(), LinearFun(0.2), AffineFun(-1, bias=9.0)],
        outcome_space=session.outcome_space,
    )

    buyer_utility = LUFun(
        values={
            "price": AffineFun(-1, bias=9.0),
            "quantity": LinearFun(0.2),
            "delivery_time": IdentityFun(),
        },
        outcome_space=session.outcome_space,
    )

    buyer = TimeBasedConcedingNegotiator(name="buyer")
    seller = TimeBasedConcedingNegotiator(name="seller")

    # create and add buyer and seller negotiators
    session.add(buyer, preferences=buyer_utility)
    session.add(seller, ufun=seller_utility)

    # run the negotiation and show the results
    result = session.run()

    buyer_offers = session.negotiator_offers(buyer.id)
    seller_offers = session.negotiator_offers(seller.id)

    fig_name = str(uuid.uuid4()) + ".png"

    session.plot(show_reserved=False, save_fig=True, fig_name=fig_name, path="static/images")
    
    data = {
        "result": result.agreement,
        "time": result.time,
        "image": fig_name,
        "a1_offers": str([tuple(int(item) for item in tup) for tup in buyer_offers]), 
        "a2_offers": str([tuple(int(item) for item in tup) for tup in seller_offers]), 
        "data": [item for item in zip(buyer_offers, seller_offers)],
        # "a1_utility": float(utility_a1), 
        # "a2_utility": float(utility_a2),
    }
    if not data['result'] or (data['result'] not in buyer_offers and data['result'] not in seller_offers):
        data['winner'] = "No Winner"
    else:
        data["winner"] = "Agent 1" if data['result'] in buyer_offers else "Agent 2"
    return data
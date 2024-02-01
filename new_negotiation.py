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

    # create and add buyer and seller negotiators
    session.add(TimeBasedConcedingNegotiator(name="buyer"), preferences=buyer_utility)
    session.add(TimeBasedConcedingNegotiator(name="seller"), ufun=seller_utility)

    # run the negotiation and show the results
    result = session.run()

    fig_name = str(uuid.uuid4()) + ".png"

    session.plot(
        show_reserved=False, 
        save_fig=True,
        fig_name=fig_name,
        path="static/images"
    )
    
    return {
        "aggrement": result.agreement,
        "resulf": result.results,
        "time": result.time,
        "image": fig_name
    }
    
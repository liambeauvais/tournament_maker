from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

from step.models import Step


def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = HttpResponse(content_type='application/pdf')
    pisa_status = pisa.CreatePDF(html, dest=result, encoding='utf-8')
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return result


def get_tournament_steps(step: Step, step_iteration: int):
    steps: list[Step] = [step]
    for i in range(1, step_iteration + 1):
        if i == step_iteration:
            break
        else:
            iterated_steps = []
            for step in steps:
                iterated_steps.extend(step.step_set.all().order_by('rank'))
            steps = iterated_steps
    return steps


def get_steps_pools(steps: list[Step], pools_by_page: int = None, is_last_step: bool = False):
    pool_count = 1
    pools = []

    for step in steps:
        step_count = 1
        for pool in step.pools.all():
            print(pool.players.order_by('-player__points').all())
            if pool.players.count() > 1:
                pools.append(
                    {
                        "object": pool,
                        "next_page": pool_count % pools_by_page == 0,
                        "rank": step.last_step.rank if is_last_step else step.rank,
                        "step_count": step_count,
                        "players": pool.players.order_by('-player__points').all(),

                    }
                )
                step_count += 1
                pool_count += 1
    return pools

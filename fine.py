"""
F.I.N.E. — Framework for Interpreting Nonliteral Expression
Compiler entry point. Four passes: LOOK IN → SPIRAL UP → FLOW OUT → RETURN
"""
import sys
import argparse
from core.state import OutputTarget
from look_in.intake import look_in
from spiral_up.router import spiral_up
from flow_out.executor import flow_out
from return_to.integrate import return_to
from growth.reporter import check_and_report


def compile_feeling(raw_input: str, target: str = "song", feedback: str = None) -> str:
    try:
        output_target = OutputTarget(target)
    except ValueError:
        output_target = OutputTarget.SONG

    print(f"\n[LOOK IN]   parsing emotional signature...")
    signature = look_in(raw_input)
    config_tag = f" | config: {signature.configuration}" if signature.configuration else ""
    compound_tag = f" | compound: {len(signature.compound_emotions)} emotions" if signature.compound_emotions else ""
    print(f"            color: {signature.color} | intensity: {signature.intensity}/10 | tags: {', '.join(signature.tags)}{config_tag}{compound_tag}")

    print(f"\n[SPIRAL UP] routing...")
    route = spiral_up(signature)
    support_tag = f" + {', '.join(route.support_voices)}" if route.support_voices else ""
    spine_tag = f" | spine: {route.tempo_spine}" if route.tempo_spine else ""
    print(f"            voice: {route.primary_voice}{support_tag}{spine_tag} | {route.reasoning}")

    print(f"\n[FLOW OUT]  generating {output_target.value}...")
    output = flow_out(signature, route, output_target)

    print(f"\n[RETURN]    integrating...")
    integration = return_to(output, feedback)

    print(f"\n{'='*60}")
    print(output.content)
    print(f"{'='*60}\n")

    if not integration.landed and integration.next_signature:
        print(f"[RETURN] didn't land — adjusting ({integration.adjustment}) and recompiling...\n")
        return compile_feeling(integration.next_signature.raw_input, target)

    report_path = check_and_report(signature, route, integration)
    if report_path:
        print(f"[GROWTH]  gap detected — report written to {report_path}")

    return output.content


def main():
    parser = argparse.ArgumentParser(description="F.I.N.E. — Framework for Interpreting Nonliteral Expression")
    parser.add_argument("input", nargs="?", help="Raw feeling input (or pipe via stdin)")
    parser.add_argument("--target", default="song",
                        choices=["song", "prose", "protocol", "boundary", "poem"],
                        help="Output type")
    parser.add_argument("--feedback", help="Integration feedback from previous run")
    args = parser.parse_args()

    if args.input:
        raw = args.input
    elif not sys.stdin.isatty():
        raw = sys.stdin.read().strip()
    else:
        print("What are you feeling? (paste or type, end with Ctrl+D)\n")
        raw = sys.stdin.read().strip()

    compile_feeling(raw, args.target, args.feedback)


if __name__ == "__main__":
    main()

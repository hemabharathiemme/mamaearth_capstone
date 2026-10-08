# narrator/generate_narrative.py
import json
import os

def run_offline_generation(findings):
    r = findings['cleaned_total_revenue_inr']
    c = findings['return_rate_by_payment']['COD']
    s = findings['highest_risk_segment']['return_rate_pct']
    d = findings['duplicate_reconciliation_delta_inr']
    p_m = findings['true_peak_month']['month']
    p_v = findings['true_peak_month']['revenue_inr']

    brief = f"""### SITUATION
Mamaearth's data pipeline has aggregated all transaction records across core regions, confirming a net cleaned baseline revenue of INR {r:,.2f}.

### COMPLICATION
Operational data audits reveal severe risk exposures across localized customer fulfillment layers. Most notably, the COD return rate stands at {c:.1f}%, driven heavily by the COD + Tier-2 highest-risk segment which maps an erosion rate of {s:.1f}%. Processing pipeline runs isolated a duplicate-driven reconciliation delta of INR {d:,.2f} from double-submit telemetry bugs. Furthermore, time-series analysis confirms early winter revenue signals were artificially inflated by bulk outliers, hiding the fact that our true peak month occurs in {p_m} with clear net revenue totals reaching INR {p_v:,.2f}.

### RESOLUTION
Risk management operations must implement automated point-of-delivery checks on all cash transactions within Tier-2 sectors. The software layer will deploy structural primary telemetry locks to drop double-submit updates before database ingestion.
"""
    return brief

def main():
    with open("narrator/findings.json", "r") as f:
        findings = json.load(f)

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("[!] GEMINI_API_KEY environment variable missing. Executing deterministic offline template...")
        narrative_txt = run_offline_generation(findings)
    else:
        try:
            from google import genai
            from google.genai import types
            
            client = genai.Client(api_key=api_key)
            instruction = "You are a senior analyst for Mamaearth reporting to Ops Heads. Format your response into explicit sections: Situation, Complication, Resolution. You must use the provided metrics exactly without alterations."
            
            prompt = f"Write an executive summary based on these pipeline figures: Cleaned Rev: {findings['cleaned_total_revenue_inr']}, COD Return Rate: {findings['return_rate_by_payment']['COD']}%, COD Tier-2 Risk: {findings['highest_risk_segment']['return_rate_pct']}%, Delta: {findings['duplicate_reconciliation_delta_inr']}, True Peak: {findings['true_peak_month']['month']} ({findings['true_peak_month']['revenue_inr']})."
            
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
                config=types.GenerateContentConfig(system_instruction=instruction, temperature=0.0, max_output_tokens=500)
            )
            narrative_txt = response.text
        except Exception as e:
            print(f"[!] Live call exception: {e}. Defaulting to offline generation...")
            narrative_txt = run_offline_generation(findings)

    print("\n=== GENERATED NARRATIVE SUMMARY ===")
    print(narrative_txt)
    
    with open("narrator/sample_output.txt", "w", encoding="utf-8") as out:
        out.write(narrative_txt)
    print("\n✓ saved summary text output file to narrator/sample_output.txt")

if __name__ == "__main__":
    main()

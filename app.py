import streamlit as st
import time
from typing import List, Dict

# The core solver logic
def crypt(addends: List[str], result: str) -> List[Dict[str, int]]:
    addends = [w[::-1].upper() for w in addends]
    result = result[::-1].upper()

    letters = set("".join(addends) + result)
    if len(letters) > 10:
        return []

    leading = set(w[-1] for w in addends + [result] if len(w) > 1)
    max_len = max(len(w) for w in addends + [result])

    assignment: Dict[str, int] = {}
    digit = set()
    s = []

    def backtrack(col: int, carry: int):
        if col == max_len:
            if carry == 0:
                s.append(assignment.copy())
            return

        add_letters = []
        for w in addends:
            if col < len(w):
                add_letters.append(w[col])

        res_letter = result[col] if col < len(result) else None

        def assign(idx: int, total: int):
            if idx == len(add_letters):
                d_val = total % 10
                next_carry = total // 10

                a = False

                if res_letter:
                    if res_letter in assignment:
                        if assignment[res_letter] != d_val:
                            return
                    else:
                        if d_val in digit:
                            return
                        if d_val == 0 and res_letter in leading:
                            return
                        assignment[res_letter] = d_val
                        digit.add(d_val)
                        a = True

                backtrack(col + 1, next_carry)

                if a:
                    del assignment[res_letter]
                    digit.remove(d_val)
                return

            letter = add_letters[idx]

            if letter in assignment:
                assign(idx + 1, total + assignment[letter])
            else:
                for d in range(10):
                    if d in digit:
                        continue
                    if d == 0 and letter in leading:
                        continue

                    assignment[letter] = d
                    digit.add(d)
                    assign(idx + 1, total + d)
                    del assignment[letter]
                    digit.remove(d)

        assign(0, carry)

    backtrack(0, 0)
    return s


# UI Configuration
st.set_page_config(page_title="Cryptarithmetic Solver", page_icon="✨", layout="centered")

# Custom CSS for glassmorphism, minimal typography, and glowing gradients
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Background gradient */
    .stApp {
        background: radial-gradient(circle at 15% 50%, #1e1e2f 0%, #12121a 100%);
        color: #e2e8f0;
    }

    /* Minimal Input fields */
    .stTextInput>div>div>input {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        color: white;
        padding: 10px 15px;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }

    .stTextInput>div>div>input:focus {
        border-color: #7b61ff;
        box-shadow: 0 0 15px rgba(123, 97, 255, 0.4);
    }
    
    /* Labels */
    .stTextInput label p {
        color: #94a3b8;
        font-weight: 500;
        font-size: 0.95rem;
    }

    /* Glowing button */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #7b61ff, #00d2ff);
        border: none;
        color: white;
        font-weight: 600;
        letter-spacing: 0.5px;
        border-radius: 12px;
        padding: 12px;
        transition: transform 0.2s, box-shadow 0.2s;
        box-shadow: 0 4px 15px rgba(123, 97, 255, 0.3);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(123, 97, 255, 0.5);
        color: white;
    }

    /* Glassmorphism Results Card */
    .result-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 24px;
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        margin-top: 20px;
        animation: fadein 0.6s ease;
    }

    .result-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px 0;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        font-family: 'Inter', monospace;
        font-size: 1.1rem;
    }
    
    .result-item:last-child {
        border-bottom: none;
    }

    .letter-badge {
        background: rgba(123, 97, 255, 0.2);
        color: #a78bfa;
        padding: 4px 12px;
        border-radius: 8px;
        font-weight: 600;
    }

    .digit-badge {
        color: #white;
        font-weight: 600;
        font-size: 1.2rem;
    }

    h1 {
        text-align: center;
        background: -webkit-linear-gradient(45deg, #00d2ff, #7b61ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        color: #8b9bb4;
        font-size: 1.1rem;
        margin-bottom: 40px;
    }

    @keyframes fadein {
        from { opacity: 0; transform: translateY(10px); }
        to   { opacity: 1; transform: translateY(0); }
    }
    
    /* Center the warning/errors nicely */
    .stAlert {
        border-radius: 12px;
        border: 1px solid rgba(255,75,75,0.4);
        background: rgba(255,75,75,0.1);
        color: #ffcccc;
    }
    </style>
""", unsafe_allow_html=True)

# Main App Structure
st.markdown("<h1>Cryptarithm Solver</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>A minimal, modern tool for solving word addition puzzles.</p>", unsafe_allow_html=True)

col1, col2 = st.columns([1.5, 1])

with col1:
    addends_input = st.text_input("Addends (comma separated)", value="TO, GO", help="Example: SEND, MORE")
with col2:
    result_input = st.text_input("Result Word", value="OUT", help="Example: MONEY")

solve_clicked = st.button("Crack the Code")

if solve_clicked:
    if not addends_input or not result_input:
        st.warning("Please provide both addends and a result word.")
    else:
        addends_list = [v.strip() for v in addends_input.split(",")]
        
        with st.spinner("Calculating combinations..."):
            # Small artificial delay to show off spinner in a fast solver
            time.sleep(0.4)
            solutions = crypt(addends_list, result_input.strip())
            
        if not solutions:
            st.error("No valid solutions found for this puzzle.")
        else:
            st.markdown("### Solution Found! ✨")
            # Only showing first solution for minimalism
            best_sol = solutions[0]
            
            # Map out the letters into a glassmorphism card
            card_html = "<div class='result-card'>"
            for letter, digit in sorted(best_sol.items()):
                card_html += f"""
                <div class='result-item'>
                    <span class='letter-badge'>{letter}</span>
                    <span class='digit-badge'>{digit}</span>
                </div>
                """
            card_html += "</div>"
            
            st.markdown(card_html, unsafe_allow_html=True)
            
            # If multiple exist, hint it delicately
            if len(solutions) > 1:
                st.caption(f"*Found {len(solutions) - 1} other valid solutions, displaying the first one.*")

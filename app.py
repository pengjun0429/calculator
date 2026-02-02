from flask import Flask, render_template, request
import re
import operator

app = Flask(__name__)

# 保留原本的運算定義與對照表
ops = {
    "+": operator.add, "-": operator.sub, 
    "*": operator.mul, "/": operator.truediv
}

# 全域變數 s 紀錄
s = {"val": None}

# 保留原本的正則表達式
pattern = re.compile(r"\s*(s|\d+(\.\d+)?)\s*([\+\-\*/])\s*(s|\d+(\.\d+)?)")

@app.route("/", methods=["GET", "POST"])
def index():
    ans_display = ""
    error_msg = ""
    
    if request.method == "POST":
        # 取得前端輸入的整串算式，例如 "s + 10" 或 "5 * 5"
        expr = request.form.get("expr", "").strip()
        
        # 1. 處理彩蛋
        if expr.lower() == "qq":
            ans_display = "✨ 發現彩蛋：別哭了 QQ ✨"
            return render_template("index.html", ans=ans_display, s_val=s["val"])

        # 2. 解析算式 (保留你的 re 邏輯)
        match = pattern.fullmatch(expr)
        if not match:
            error_msg = "❌ 無效算式，請輸入如 '5 + 5' 或 's * 2'"
        else:
            a_str, op, b_str = match.group(1), match.group(3), match.group(4)
            
            try:
                # 3. 轉換數字 (s 或是 float)
                val_a = s["val"] if a_str == "s" else float(a_str)
                val_b = s["val"] if b_str == "s" else float(b_str)

                if val_a is None or val_b is None:
                    error_msg = "❌ 目前無紀錄，請先輸入數字運算"
                else:
                    # 4. 執行運算
                    if op == "/" and val_b == 0:
                        error_msg = "❌ 錯誤：不能除以零！"
                    else:
                        ans = ops[op](val_a, val_b)
                        ans_display = f"{val_a} {op} {val_b} = {ans}"
                        
                        # 5. 更新 s 紀錄 (這就是你 py 裡的 s = ans)
                        s["val"] = ans
                        
            except Exception as e:
                error_msg = f"發生錯誤: {e}"

    return render_template("index.html", ans=ans_display, error=error_msg, s_val=s["val"])

if __name__ == "__main__":
    app.run(debug=True)

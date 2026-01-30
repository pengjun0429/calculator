from flask import Flask, render_template, request
#看好,這是必須的
import operator
#--------------------

app = Flask(__name__)

# ???不知道
ops = {
    "加": (operator.add, "+"), "+": (operator.add, "+"),
    "減": (operator.sub, "-"), "-": (operator.sub, "-"),
    "乘": (operator.mul, "*"), "*": (operator.mul, "*"),
    "除": (operator.truediv, "/"), "/": (operator.truediv, "/")
}

# 全域變數
s = {"val": None}

@app.route("/", methods=["GET", "POST"])
def index():
    ans_display = ""
    error_msg = ""
    
    if request.method == "POST":
        action = request.form.get("action")
        
        # 處理儲存邏輯
        if action == "save":
            current_ans = request.form.get("current_ans")
            if current_ans:
                s["val"] = float(current_ans)
                ans_display = f"(已儲存) 目前紀錄為: {s['val']}"
            return render_template("index.html", ans=ans_display, s_val=s["val"])

        # 1. 選擇模式
        mode = request.form.get("mode").strip()
        
        # 彩蛋
        if mode.lower() == 'qq':
            ans_display = "別哭"
            return render_template("index.html", ans=ans_display, s_val=s["val"])
            
        if mode not in ops:
            error_msg = "❌ 輸入錯誤,請重新選擇。"
            return render_template("index.html", error=error_msg, s_val=s["val"])

        # 2. 取得數字 
        try:
            raw_st = request.form.get("st").strip().lower()
            raw_nd = request.form.get("nd").strip().lower()
            
            st = s["val"] if raw_st == 's' else float(raw_st)
            nd = s["val"] if raw_nd == 's' else float(raw_nd)
            
            if st is None or nd is None:
                error_msg = "❌ 目前無儲存紀錄，請輸入數字。"
                return render_template("index.html", error=error_msg, s_val=s["val"])

            # 3. 執行運算
            func, symbol = ops[mode]
            
            # 處理除以零:)
            if symbol == "/" and nd == 0:
                error_msg = "❌ 錯誤：不能除以零！"
            else:
                result = func(st, nd)
                # 4. 結果
                ans_display = f"計算結果: {st} {symbol} {nd} = {result}"
                return render_template("index.html", ans=ans_display, raw_res=result, s_val=s["val"])
        
        except ValueError:
            error_msg = "⚠️ 請輸入有效的數字，或輸入 's' 使用上一次結果。"

    return render_template("index.html", error=error_msg, s_val=s["val"])

#辛承霖你別管
if __name__ == "__main__":
    app.run(debug=True)
import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.time.LocalDate;
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        //キーボードから入力を受け取るためScannerを初期化
        Scanner scanner = new Scanner(System.in);
        
        System.out.println("=== 学習記録アプリ ===");
        
        // 記録日の日付を自動取得する
        LocalDate today = LocalDate.now();
        System.out.print("日付を入力してください (例: " + today + ") [Enterのみで今日]: ");
        String dateInput = scanner.nextLine().trim();//前後の余分な空白を削除
        //入力が空なら今日の日付を、入力があればその文字列を使用
        String recordDate = dateInput.isEmpty() ? today.toString() : dateInput;

        // 学習内容の入力
        System.out.print("学習内容を入力してください (例: Java, Python等): ");
        String content = scanner.nextLine().trim();

        // 学習時間の入力
        //例外処理による堅労性の確保
        System.out.print("勉強時間（時間）を入力してください (例: 2.5): ");
        double hours = 0.0;
        try {
            //文字列として受け取ったものをdouble型に変換
            hours = Double.parseDouble(scanner.nextLine().trim());
        } catch (NumberFormatException e) {
            //エラーになる入力でも強制終了を防ぐ
            System.out.println(" 数値が正しく入力されなかったため、時間は 0.0 で記録します。");
        }

        // ひとつのテキスト行としてまとめる形式
        // 例: 日付: 2026-05-10, 内容: Java, 時間: 2.5
        String logLine = "日付: " + recordDate + ", 内容: " + content + ", 時間: " + hours;

        // study_log.txt に追記保存する
        //ファイルへの永続化処理
        try (BufferedWriter writer = new BufferedWriter(new FileWriter("study_log.txt", true))) {
            writer.write(logLine);
            writer.newLine();//改行コードの挿入
            System.out.println("\n 記録を 'study_log.txt' に保存しました！");
        } catch (IOException e) {
            //ファイル書き込み時の入出力エラーをキャッチするためのもの
            System.out.println(" ファイルの書き込み中にエラーが発生しました: " + e.getMessage());
        }
        
        scanner.close();
        //リソースリークを防ぐためのスキャナーを閉じる
    }
}
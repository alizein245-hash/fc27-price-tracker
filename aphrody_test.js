
import { handleAnyFutUrl } from "@aphrody/fut";

const playerUrl =
  "https://www.futbin.com/27/player/21977/bradley-barcola";

console.log("=".repeat(70));
console.log("APHRODY / FUTBIN TEST");
console.log("=".repeat(70));
console.log();
console.log("Spieler: Bradley Barcola");
console.log("FUTBIN ID: 21977");
console.log("URL:", playerUrl);
console.log();
console.log("Starte FUTBIN-Abfrage...");
console.log();

try {
  const result = await handleAnyFutUrl(playerUrl);

  console.log();
  console.log("=".repeat(70));
  console.log("ROHES ERGEBNIS");
  console.log("=".repeat(70));
  console.log();

  console.log(JSON.stringify(result, null, 2));

  console.log();
  console.log("=".repeat(70));
  console.log("TEST ABGESCHLOSSEN");
  console.log("=".repeat(70));

} catch (error) {
  console.log();
  console.log("=".repeat(70));
  console.log("FEHLER");
  console.log("=".repeat(70));
  console.log();

  console.error(error);

  process.exit(1);
}

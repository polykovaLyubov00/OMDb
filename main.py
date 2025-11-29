import requests
import time
import json
from datetime import datetime


class OMDBApiTester:
    def __init__(self):
        self.api_key = "1204d6f5"
        self.base_url = "http://www.omdbapi.com/"
        self.results = []

    def make_request(self, params):
        """Делает запрос к API"""
        try:
            # Всегда добавляем API ключ
            all_params = params.copy()
            all_params['apikey'] = self.api_key

            # Замеряем время
            start_time = time.time()
            response = requests.get(self.base_url, params= all_params, timeout= 10)
            end_time = time.time()

            response_time = round((end_time - start_time) * 1000, 2)

            return {
                "success": True,
                "data": response.json(),
                "response_time": response_time,
                "status_code": response.status_code
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def print_test_result(self, test_name, is_success, details=""):
        """Печатает результат теста"""
        if is_success:
            print(f"✅ {test_name}: ПРОЙДЕН - {details}")
        else:
            print(f"❌ {test_name}: НЕ ПРОЙДЕН - {details}")

    def save_result(self, test_name, expected, actual, status):
        """Сохраняет результат теста"""
        self.results.append({
            "test_name": test_name,
            "expected": expected,
            "actual": actual,
            "status": status,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

    def test_basic_functionality(self):
        """Тестирует базовую функциональность API"""
        print("\n" + "=" * 50)
        print("1. БАЗОВОЕ ТЕСТИРОВАНИЕ")
        print("=" * 50)

        # Тест 1: Проверка доступности API
        result = self.make_request({"s": "test"})
        if result["success"]:
            self.print_test_result("Доступность API", True, f"Время ответа: {result['response_time']}ms")
            self.save_result("Доступность API", "Успешный ответ", "Успешный ответ", "PASS")
        else:
            self.print_test_result("Доступность API", False, result["error"])
            self.save_result("Доступность API", "Успешный ответ", result["error"], "FAIL")

        # Тест 2: Поиск фильма
        result = self.make_request({"s": "Matrix"})
        if result["success"] and result["data"].get("Response") == "True":
            movies_count = len(result["data"].get("Search", []))
            self.print_test_result("Поиск фильма", True, f"Найдено фильмов: {movies_count}")
            self.save_result("Поиск фильма", "Найденные фильмы", f"Найдено {movies_count} фильмов", "PASS")
        else:
            self.print_test_result("Поиск фильма", False, "Фильмы не найдены")
            self.save_result("Поиск фильма", "Найденные фильмы", "Фильмы не найдены", "FAIL")

    def test_movie_details(self):
        """Тестирует получение деталей фильма"""
        print("\n" + "=" * 50)
        print("2. ДЕТАЛИ ФИЛЬМА")
        print("=" * 50)

        # Тест 1: Детали по ID
        result = self.make_request({"i": "tt0133093"})
        if result["success"] and result["data"].get("Response") == "True":
            title = result["data"].get("Title", "")
            year = result["data"].get("Year", "")
            self.print_test_result("Детали по ID", True, f"Фильм: {title} ({year})")
            self.save_result("Детали по ID", "Информация о фильме", f"Найден {title}", "PASS")
        else:
            self.print_test_result("Детали по ID", False, "Фильм не найден")
            self.save_result("Детали по ID", "Информация о фильме", "Фильм не найден", "FAIL")
            # Тест 2: Детали по названию
            result = self.make_request({"t": "Inception"})
            if result["success"] and result["data"].get("Response") == "True":
                title = result["data"].get("Title", "")
                self.print_test_result("Детали по названию", True, f"Фильм: {title}")
                self.save_result("Детали по названию", "Информация о фильме", f"Найден {title}", "PASS")
            else:
                self.print_test_result("Детали по названию", False, "Фильм не найден")
                self.save_result("Детали по названию", "Информация о фильме", "Фильм не найден", "FAIL")

    def test_error_handling(self):
        """Тестирует обработку ошибок"""
        print("\n" + "=" * 50)
        print("3. ОБРАБОТКА ОШИБОК")
        print("=" * 50)

        # Тест 1: Несуществующий фильм
        result = self.make_request({"s": "ThisMovieDoesNotExist123456"})
        if result["success"] and result["data"].get("Response") == "False":
            error_msg = result["data"].get("Error", "")
            self.print_test_result("Несуществующий фильм", True, f"Ошибка: {error_msg}")
            self.save_result("Несуществующий фильм", "Сообщение об ошибке", error_msg, "PASS")
        else:
            self.print_test_result("Несуществующий фильм", False, "Некорректный ответ")
            self.save_result("Несуществующий фильм", "Сообщение об ошибке", "Некорректный ответ", "FAIL")

        # Тест 2: Неверный ID
        result = self.make_request({"i": "invalid_id"})
        if result["success"] and result["data"].get("Response") == "False":
            self.print_test_result("Неверный ID", True, "Корректная обработка ошибки")
            self.save_result("Неверный ID", "Сообщение об ошибке", "Ошибка обработана", "PASS")
        else:
            self.print_test_result("Неверный ID", False, "Некорректный ответ")
            self.save_result("Неверный ID", "Сообщение об ошибке", "Некорректный ответ", "FAIL")

    def test_filters(self):
        """Тестирует фильтры"""
        print("\n" + "=" * 50)
        print("4. ФИЛЬТРЫ")
        print("=" * 50)

        # Тест 1: Фильтр по году
        result = self.make_request({"s": "batman", "y": "2005"})
        if result["success"]:
            if result["data"].get("Response") == "True":
                movies_count = len(result["data"].get("Search", []))
                self.print_test_result("Фильтр по году", True, f"Найдено: {movies_count}")
                self.save_result("Фильтр по году", "Отфильтрованные результаты", f"Найдено {movies_count}", "PASS")
            else:
                self.print_test_result("Фильтр по году", True, "Нет результатов")
                self.save_result("Фильтр по году", "Отфильтрованные результаты", "Нет результатов", "PASS")
        else:
            self.print_test_result("Фильтр по году", False, result["error"])
            self.save_result("Фильтр по году", "Отфильтрованные результаты", result["error"], "FAIL")

        # Тест 2: Фильтр по типу
        result = self.make_request({"s": "planet", "type": "series"})
        if result["success"]:
            if result["data"].get("Response") == "True":
                movies = result["data"].get("Search", [])
                all_series = all(movie.get("Type") == "series" for movie in movies)
                if all_series:
                    self.print_test_result("Фильтр по типу", True, f"Все результаты - сериалы: {len(movies)}")
                    self.save_result("Фильтр по типу", "Только сериалы", f"Найдено {len(movies)} сериалов", "PASS")
                else:
                    self.print_test_result("Фильтр по типу", False, "Не все результаты - сериалы")
                    self.save_result("Фильтр по типу", "Только сериалы", "Не все результаты - сериалы", "FAIL")
            else:
                self.print_test_result("Фильтр по типу", True, "Нет результатов")
                self.save_result("Фильтр по типу", "Только сериалы", "Нет результатов", "PASS")
        else:
            self.print_test_result("Фильтр по типу", False, result["error"])
            self.save_result("Фильтр по типу", "Только сериалы", result["error"], "FAIL")

    def test_pagination(self):
        """Тестирует пагинацию"""
        print("\n" + "=" * 50)
        print("5. ПАГИНАЦИЯ")
        print("=" * 50)

        # Тест 1: Первая страница
        result1 = self.make_request({"s": "test", "page": 1})
        # Тест 2: Вторая страница
        result2 = self.make_request({"s": "test", "page": 2})

        if result1["success"] and result2["success"]:
            data1 = result1["data"]
            data2 = result2["data"]

            if data1.get("Response") == "True" and data2.get("Response") == "True":
                movies1 = data1.get("Search", [])
                movies2 = data2.get("Search", [])

                if len(movies1) > 0 and len(movies2) > 0:
                    self.print_test_result("Пагинация", True, f"Страница 1: {len(movies1)}, Страница 2: {len(movies2)}")
                    self.save_result("Пагинация", "Разные страницы", "Пагинация работает", "PASS")
                else:
                    self.print_test_result("Пагинация", True, "Мало данных для теста")
                    self.save_result("Пагинация", "Разные страницы", "Мало данных", "PASS")
            else:
                self.print_test_result("Пагинация", True, "Нет результатов")
                self.save_result("Пагинация", "Разные страницы", "Нет результатов", "PASS")
        else:
            self.print_test_result("Пагинация", False, "Ошибка запроса")
            self.save_result("Пагинация", "Разные страницы", "Ошибка запроса", "FAIL")

    def test_performance(self):
        """Тестирует производительность"""
        print("\n" + "=" * 50)
        print("6. ПРОИЗВОДИТЕЛЬНОСТЬ")
        print("=" * 50)

        # Тест времени ответа
        result = self.make_request({"s": "test"})
        if result["success"]:
            response_time = result["response_time"]
            if response_time < 2000:  # 2 секунды
                self.print_test_result("Время ответа", True, f"{response_time}ms")
                self.save_result("Время ответа", "< 2000ms", f"{response_time}ms", "PASS")
            else:
                self.print_test_result("Время ответа", False, f"Медленно: {response_time}ms")
                self.save_result("Время ответа", "< 2000ms", f"{response_time}ms", "FAIL")
        else:
            self.print_test_result("Время ответа", False, result["error"])
            self.save_result("Время ответа", "< 2000ms", result["error"], "FAIL")

    def run_all_tests(self):
        """Запускает все тесты"""
        print("🚀 ЗАПУСК ТЕСТИРОВАНИЯ OMDB API")
        print(f"🔑 API Key: {self.api_key}")
        print(f"🌐 Base URL: {self.base_url}")
        print("=" * 60)

        # Запускаем все тесты
        self.test_basic_functionality()
        self.test_movie_details()
        self.test_error_handling()
        self.test_filters()
        self.test_pagination()
        self.test_performance()

        # Показываем итоги
        self.show_summary()

    def show_summary(self):
        """Показывает итоговую статистику"""
        print("\n" + "=" * 60)
        print("📊 ИТОГИ ТЕСТИРОВАНИЯ")
        print("=" * 60)

        total_tests = len(self.results)
        assed_tests = sum(1 for result in self.results if result["status"] == "PASS")
        failed_tests = sum(1 for result in self.results if result["status"] == "FAIL")

        print(f"Всего тестов: {total_tests}")
        print(f"✅ Пройдено: {assed_tests}")
        print(f"❌ Не пройдено: {failed_tests}")

        if total_tests > 0:
            success_rate = (assed_tests / total_tests) * 100
            print(f"📈 Успешность: {success_rate:.1f}%")

        # Сохраняем результаты в файл
        try:
            with open("omdb_test_results.json", "w", encoding="utf-8") as f:
                json.dump(self.results, f, indent=2, ensure_ascii=False, default=str)
            print("💾 Результаты сохранены в: omdb_test_results.json")
        except Exception as e:
            print(f"⚠️ Ошибка при сохранении результатов: {e}")

# Главная функция для запуска
def main():
    """Основная функция для запуска тестов"""
    tester = OMDBApiTester()
    tester.run_all_tests()

# Запуск программы
if __name__ == "__main__":
    main()
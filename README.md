# Business Performance & Inventory Management - Tiki E-commerce Data Analysis

## Overview

This project analyzes product data from Tiki, Vietnam's leading e-commerce platform, to provide insights into business performance and inventory management. The analysis focuses on 41,603 products across 6 categories: backpacks & suitcases, fashion accessories, men's bags, men's shoes, women's bags, and women's shoes.

## Project Structure

```
Business Performance & Inventory Management/
├── README.md                    # Project documentation
├── requirements.txt             # Python dependencies
├── data/                        # Raw data files (6 CSV files)
├── notebook/                    # Jupyter notebooks
│   ├── 01_data_cleaning.ipynb   # Data preprocessing pipeline
│   ├── 02_EDA.ipynb            # Exploratory data analysis
│   └── tiki_analyst.ipynb      # Original analysis notebook
├── src/                        # Modular Python code
│   ├── config.py               # Configuration and constants
│   ├── preprocessing.py        # Data loading and cleaning functions
│   ├── visualization.py        # Plotting and visualization functions
│   ├── inventory_analysis.py   # Inventory health and recommendations
│   └── performance_analysis.py # Product performance scoring and ranking
└── reports/                    # Generated reports and outputs
```

## Data Sources

The dataset consists of 6 CSV files containing Vietnamese Tiki product information:

- `vietnamese_tiki_products_backpacks_suitcases.csv`
- `vietnamese_tiki_products_fashion_accessories.csv`
- `vietnamese_tiki_products_men_bags.csv`
- `vietnamese_tiki_products_men_shoes.csv`
- `vietnamese_tiki_products_women_bags.csv`
- `vietnamese_tiki_products_women_shoes.csv`

### Key Data Fields

- **Product Info**: id, name, category, brand, description
- **Pricing**: original_price, price, discount_pct
- **Performance**: rating_average, review_count, favourite_count
- **Sales**: quantity_sold (interpreted as cumulative sales volume)
- **Fulfillment**: fulfillment_type, pay_later
- **Content**: number_of_images, has_video, vnd_cashback
- **Seller**: current_seller
- **Temporal**: date_created (product creation date)

## Business Objectives

1. **Inventory Optimization**: Identify slow-moving and fast-moving inventory
2. **Performance Analysis**: Rank products and categories by business metrics
3. **Pricing Strategy**: Analyze discount impact and pricing patterns
4. **Category Insights**: Compare performance across product categories
5. **Seller Benchmarking**: Evaluate seller performance and market positioning

## Analysis Workflow

### 1. Data Preprocessing (`01_data_cleaning.ipynb`)

- Load and combine all CSV files
- Remove unnecessary columns (e.g., 'Unnamed: 0')
- Handle missing values (drop rows with nulls)
- Remove duplicate entries based on product ID
- Validate price consistency (original_price ≥ price)
- Normalize category formats
- Extract features from descriptions
- Engineer business-relevant features (discounts, product age, composite scores)

### 2. Exploratory Data Analysis (`02_EDA.ipynb`)

- Price distribution analysis by category
- Rating and review count heatmaps
- Inventory vs performance scatter plots
- Sales trends over time (if temporal data available)
- Fulfillment type impact analysis
- Correlation analysis of numeric features
- Category-level performance comparisons

### 3. Inventory Analysis (`inventory_analysis.py`)

- Calculate inventory turnover ratios
- Identify slow-moving products (low sales volume)
- Identify fast-moving products (high sales volume)
- Generate restock priority recommendations
- Assess inventory health scores
- Analyze inventory metrics by category
- Simple demand forecasting

### 4. Performance Analysis (`performance_analysis.py`)

- Calculate composite performance scores
- Rank products by overall performance
- Identify top-selling products
- Analyze brand performance metrics
- Compare category-level trends
- Evaluate seller performance
- Identify performance outliers
- Estimate ROI for products

## Key Metrics and KPIs

### Performance Metrics
- **Composite Score**: Weighted combination of rating, reviews, favorites, sales, and discounts
- **Sales Volume**: Total quantity sold (cumulative)
- **Customer Engagement**: Review count, favorite count, rating average
- **Pricing Effectiveness**: Discount percentage, price positioning

### Inventory Metrics
- **Turnover Rate**: Sales velocity over time
- **Stock Health**: Combination of sales volume and customer satisfaction
- **Restock Priority**: Weighted score for inventory replenishment decisions

### Business KPIs
- **Category Market Share**: Sales distribution across categories
- **Top Performer Identification**: Products exceeding performance thresholds
- **Seller Rankings**: Performance comparison across sellers
- **ROI Estimates**: Profitability analysis (simplified)

## Installation and Setup

1. **Clone or download the project**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the analysis**:
   - Start with `01_data_cleaning.ipynb` for data preprocessing
   - Continue with `02_EDA.ipynb` for exploratory analysis
   - Use modular functions in `src/` for custom analyses

## Usage Examples

### Basic Data Loading
```python
from src.preprocessing import preprocess_data

df = preprocess_data()
print(f"Loaded {len(df)} products across {df['main_category'].nunique()} categories")
```

### Performance Analysis
```python
from src.performance_analysis import calculate_product_score, rank_products_by_performance

df = calculate_product_score(df)
top_products = rank_products_by_performance(df, top_n=10)
```

### Inventory Assessment
```python
from src.inventory_analysis import identify_slow_movers, recommend_restock_priorities

df = identify_slow_movers(df)
df = recommend_restock_priorities(df)
```

### Visualization
```python
from src.visualization import plot_price_distributions_by_category, plot_correlation_matrix

plot_price_distributions_by_category(df)
plot_correlation_matrix(df)
```

## Business Insights and Recommendations

### Inventory Management
- Focus restocking efforts on high-priority products (based on sales velocity and customer ratings)
- Monitor slow-moving inventory for potential clearance or discontinuation
- Optimize stock levels based on turnover analysis

### Performance Optimization
- Prioritize marketing efforts on top-performing products and categories
- Use performance scores to guide product development decisions
- Benchmark against top sellers for competitive analysis

### Pricing Strategy
- Analyze discount impact on sales volume and customer engagement
- Identify optimal price points within categories
- Monitor pricing consistency and competitiveness

### Category Strategy
- Allocate resources based on market share and growth potential
- Identify cross-category opportunities and trends
- Focus on high-performing categories for expansion

## Limitations and Assumptions

- **Sales Interpretation**: `quantity_sold` is assumed to represent cumulative sales volume
- **Temporal Analysis**: Limited by `date_created` field availability and granularity
- **Cost Estimation**: ROI calculations use simplified cost assumptions (60% of revenue)
- **Data Freshness**: Analysis based on snapshot data without real-time updates
- **Market Coverage**: Analysis limited to 6 product categories

## Advanced Analysis Features

### 1. Business Performance Analysis

#### Pareto Principle (80/20 Rule)
- Identifies top 20% products generating 80% of sales/reviews
- Category-level analysis for strategic focus
- Helps prioritize marketing and inventory efforts

#### Discount Effectiveness Analysis
- Correlates discount percentages with sales performance
- Analyzes impact on customer engagement metrics
- Provides insights for pricing strategy optimization

#### Brand Equity Analysis
- Compares performance between branded vs. no-brand products
- Calculates brand premium metrics (price, rating, sales differences)
- Identifies top-performing brands for partnership opportunities

### 2. Inventory Management Enhancements

#### ABC Classification
- **Category A**: High-value products (top 80% cumulative value) - Tight control
- **Category B**: Medium-value products (next 15%) - Moderate control
- **Category C**: Low-value products (bottom 5%) - Minimal control
- Enables focused inventory management strategies

#### Stock-out Risk Estimation
- Uses sales velocity and product age data
- Classifies products as Low/Medium/High risk
- Helps prevent lost sales from stock-outs

#### SKU Rationalization
- Identifies categories with excessive low-performing products
- Recommends SKU reduction opportunities
- Optimizes product portfolio for better inventory efficiency

### 3. New Utility Modules

#### metrics.py
- ROI calculation functions
- Customer satisfaction scoring
- Inventory turnover metrics
- Conversion rate estimation
- Price elasticity calculations

#### utils.py
- Vietnamese text processing and cleaning
- Currency formatting (VND)
- Data validation utilities
- Logging functionality
- Safe mathematical operations

#### dashboard.py (Optional)
- Interactive Streamlit dashboard
- Real-time analysis visualization
- Category-specific insights
- Performance metrics monitoring

## Enhanced Analysis Workflow

### 1. Advanced Preprocessing
```python
from src.preprocessing import preprocess_data
df = preprocess_data()  # Now includes description features and age calculations
```

### 2. Performance Insights
```python
from src.performance_analysis import analyze_pareto_principle, analyze_discount_effectiveness
pareto_results = analyze_pareto_principle(df)
discount_analysis = analyze_discount_effectiveness(df)
```

### 3. Inventory Optimization
```python
from src.inventory_analysis import perform_abc_analysis, analyze_sku_rationalization
df_abc = perform_abc_analysis(df)
sku_recommendations = analyze_sku_rationalization(df)
```

### 4. Business Metrics
```python
from src.metrics import calculate_roi, calculate_customer_satisfaction_score
roi = calculate_roi(revenue=1000000, cost=600000)  # 67% ROI
satisfaction = calculate_customer_satisfaction_score(rating=4.5, review_count=100)
```

## Sample Advanced Insights

Based on the analysis of 41,573 Tiki products:

- **ABC Classification**: 2,252 A-items (5.4%), 4,657 B-items (11.2%), 34,664 C-items (83.4%)
- **Pareto Analysis**: Multiple categories follow 80/20 rule closely
- **Discount Impact**: Moderate correlation between discount levels and sales volume
- **Brand Premium**: Branded products show consistent performance advantages
- **SKU Opportunities**: Identified categories with potential for portfolio optimization

## Running the Dashboard

```bash
pip install streamlit
streamlit run src/dashboard.py
```

The dashboard provides:
- Interactive performance metrics
- Category-specific analysis
- Inventory health monitoring
- Real-time insights visualization

## Technologies Used

This project leverages the following technologies and libraries:

### Core Libraries
- **[Python](https://www.python.org/)** - Programming language
- **[pandas](https://pandas.pydata.org/)** - Data manipulation and analysis
- **[NumPy](https://numpy.org/)** - Numerical computing
- **[Matplotlib](https://matplotlib.org/)** - Data visualization
- **[Seaborn](https://seaborn.pydata.org/)** - Statistical data visualization
- **[scikit-learn](https://scikit-learn.org/)** - Machine learning utilities

### Development Tools
- **[Jupyter Notebook](https://jupyter.org/)** - Interactive computing environment
- **[IPython](https://ipython.readthedocs.io/en/stable/)** - Enhanced Python shell
- **[Streamlit](https://streamlit.io/)** - Web app framework for data applications

### Data Sources
- **Tiki E-commerce Platform** - Vietnamese online marketplace data

## Contributing

To contribute to this project:
1. Follow the modular structure in `src/`
2. Add comprehensive docstrings to new functions
3. Update this README with new features and insights
4. Test changes on sample data before committing

## License

This project is for educational and analytical purposes. Please ensure compliance with Tiki's terms of service and data usage policies.

---

# README (Tiếng Việt)

# Quản lý Hiệu suất Kinh doanh & Kho hàng - Phân tích Dữ liệu Tiki

## Tổng quan

Dự án này phân tích dữ liệu sản phẩm từ Tiki, nền tảng thương mại điện tử hàng đầu Việt Nam, để cung cấp insights về hiệu suất kinh doanh và quản lý kho hàng. Phân tích tập trung vào 41.603 sản phẩm trên 6 danh mục: túi xách & vali, phụ kiện thời trang, túi nam, giày nam, túi nữ, và giày nữ.

## Cấu trúc Dự án

```
Business Performance & Inventory Management/
├── README.md                    # Tài liệu dự án
├── requirements.txt             # Các thư viện Python cần thiết
├── data/                        # File dữ liệu thô (6 file CSV)
├── notebook/                    # Jupyter notebooks
│   ├── 01_data_cleaning.ipynb   # Pipeline xử lý dữ liệu
│   ├── 02_EDA.ipynb            # Phân tích khám phá dữ liệu
│   └── tiki_analyst.ipynb      # Notebook phân tích gốc
├── src/                        # Code Python module
│   ├── config.py               # Cấu hình và hằng số
│   ├── preprocessing.py        # Hàm tải và làm sạch dữ liệu
│   ├── visualization.py        # Hàm vẽ biểu đồ và trực quan hóa
│   ├── inventory_analysis.py   # Phân tích sức khỏe kho và khuyến nghị
│   └── performance_analysis.py # Đánh giá hiệu suất sản phẩm và xếp hạng
└── reports/                    # Báo cáo và đầu ra được tạo
```

## Nguồn Dữ liệu

Bộ dữ liệu bao gồm 6 file CSV chứa thông tin sản phẩm Tiki Việt Nam:

- `vietnamese_tiki_products_backpacks_suitcases.csv`
- `vietnamese_tiki_products_fashion_accessories.csv`
- `vietnamese_tiki_products_men_bags.csv`
- `vietnamese_tiki_products_men_shoes.csv`
- `vietnamese_tiki_products_women_bags.csv`
- `vietnamese_tiki_products_women_shoes.csv`

### Các Trường Dữ liệu Chính

- **Thông tin Sản phẩm**: id, name, category, brand, description
- **Giá cả**: original_price, price, discount_pct
- **Hiệu suất**: rating_average, review_count, favourite_count
- **Doanh số**: quantity_sold (được hiểu là khối lượng bán tích lũy)
- **Đặt hàng**: fulfillment_type, pay_later
- **Nội dung**: number_of_images, has_video, vnd_cashback
- **Người bán**: current_seller
- **Thời gian**: date_created (ngày tạo sản phẩm)

## Mục tiêu Kinh doanh

1. **Tối ưu hóa Kho hàng**: Xác định hàng tồn động chậm và nhanh
2. **Phân tích Hiệu suất**: Xếp hạng sản phẩm và danh mục theo chỉ số kinh doanh
3. **Chiến lược Giá**: Phân tích tác động giảm giá và mô hình giá
4. **Insights Danh mục**: So sánh hiệu suất giữa các danh mục sản phẩm
5. **Đánh giá Người bán**: Đánh giá hiệu suất người bán và vị thế thị trường

## Quy trình Phân tích

### 1. Xử lý Dữ liệu (`01_data_cleaning.ipynb`)

- Tải và kết hợp tất cả file CSV
- Loại bỏ cột không cần thiết (ví dụ: 'Unnamed: 0')
- Xử lý giá trị thiếu (loại bỏ hàng có null)
- Loại bỏ mục trùng lặp dựa trên ID sản phẩm
- Xác thực tính nhất quán giá (original_price ≥ price)
- Chuẩn hóa định dạng danh mục
- Trích xuất đặc trưng từ mô tả
- Kỹ thuật đặc trưng liên quan kinh doanh (giảm giá, tuổi sản phẩm, điểm tổng hợp)

### 2. Phân tích Khám phá Dữ liệu (`02_EDA.ipynb`)

- Phân tích phân phối giá theo danh mục
- Biểu đồ nhiệt đánh giá và số lượng đánh giá
- Biểu đồ phân tán kho vs hiệu suất
- Xu hướng bán hàng theo thời gian (nếu có dữ liệu thời gian)
- Phân tích tác động loại thực hiện đơn hàng
- Phân tích tương quan các đặc trưng số
- So sánh hiệu suất cấp danh mục

### 3. Phân tích Kho hàng (`inventory_analysis.py`)

- Tính tỷ lệ luân chuyển kho
- Xác định sản phẩm tồn động chậm (khối lượng bán thấp)
- Xác định sản phẩm tồn động nhanh (khối lượng bán cao)
- Tạo khuyến nghị ưu tiên nhập hàng
- Đánh giá điểm sức khỏe kho
- Phân tích chỉ số kho theo danh mục
- Dự báo nhu cầu đơn giản

### 4. Phân tích Hiệu suất (`performance_analysis.py`)

- Tính điểm hiệu suất tổng hợp
- Xếp hạng sản phẩm theo hiệu suất tổng thể
- Xác định sản phẩm bán chạy nhất
- Phân tích chỉ số hiệu suất thương hiệu
- So sánh xu hướng cấp danh mục
- Đánh giá hiệu suất người bán
- Xác định ngoại lệ hiệu suất
- Ước tính ROI cho sản phẩm

## Chỉ số và KPIs Chính

### Chỉ số Hiệu suất
- **Điểm Tổng hợp**: Kết hợp có trọng số của đánh giá, đánh giá, yêu thích, bán hàng và giảm giá
- **Khối lượng Bán**: Tổng số lượng đã bán (tích lũy)
- **Tương tác Khách hàng**: Số lượng đánh giá, số yêu thích, đánh giá trung bình
- **Hiệu quả Giá**: Phần trăm giảm giá, định vị giá

### Chỉ số Kho hàng
- **Tỷ lệ Luân chuyển**: Tốc độ bán theo thời gian
- **Sức khỏe Kho**: Kết hợp khối lượng bán và sự hài lòng khách hàng
- **Ưu tiên Nhập hàng**: Điểm có trọng số cho việc bổ sung kho

### KPIs Kinh doanh
- **Thị phần Danh mục**: Phân phối bán hàng giữa các danh mục
- **Xác định Người biểu diễn Xuất sắc**: Sản phẩm vượt ngưỡng hiệu suất
- **Xếp hạng Người bán**: So sánh hiệu suất giữa người bán
- **Ước tính ROI**: Phân tích lợi nhuận (đơn giản hóa)

## Cài đặt và Thiết lập

1. **Clone hoặc tải dự án**

2. **Cài đặt thư viện phụ thuộc**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Chạy phân tích**:
   - Bắt đầu với `01_data_cleaning.ipynb` để xử lý dữ liệu
   - Tiếp tục với `02_EDA.ipynb` để phân tích khám phá
   - Sử dụng hàm module trong `src/` cho phân tích tùy chỉnh

## Ví dụ Sử dụng

### Tải Dữ liệu Cơ bản
```python
from src.preprocessing import preprocess_data

df = preprocess_data()
print(f"Đã tải {len(df)} sản phẩm trên {df['main_category'].nunique()} danh mục")
```

### Phân tích Hiệu suất
```python
from src.performance_analysis import calculate_product_score, rank_products_by_performance

df = calculate_product_score(df)
top_products = rank_products_by_performance(df, top_n=10)
```

### Đánh giá Kho hàng
```python
from src.inventory_analysis import identify_slow_movers, recommend_restock_priorities

df = identify_slow_movers(df)
df = recommend_restock_priorities(df)
```

### Trực quan hóa
```python
from src.visualization import plot_price_distributions_by_category, plot_correlation_matrix

plot_price_distributions_by_category(df)
plot_correlation_matrix(df)
```

## Insights và Khuyến nghị Kinh doanh

### Quản lý Kho hàng
- Tập trung nỗ lực nhập hàng vào sản phẩm ưu tiên cao (dựa trên tốc độ bán và đánh giá khách hàng)
- Giám sát hàng tồn động chậm để thanh lý hoặc ngừng sản xuất tiềm năng
- Tối ưu hóa mức tồn kho dựa trên phân tích luân chuyển

### Tối ưu hóa Hiệu suất
- Ưu tiên nỗ lực marketing cho sản phẩm và danh mục biểu diễn xuất sắc
- Sử dụng điểm hiệu suất để hướng dẫn quyết định phát triển sản phẩm
- Điểm chuẩn với người bán hàng đầu để phân tích cạnh tranh

### Chiến lược Giá
- Phân tích tác động giảm giá lên khối lượng bán và tương tác khách hàng
- Xác định điểm giá tối ưu trong danh mục
- Giám sát tính nhất quán và cạnh tranh giá

### Chiến lược Danh mục
- Phân bổ nguồn lực dựa trên thị phần và tiềm năng tăng trưởng
- Xác định cơ hội liên danh mục và xu hướng
- Tập trung vào danh mục biểu diễn cao để mở rộng

## Hạn chế và Giả định

- **Giải thích Bán hàng**: `quantity_sold` được giả định đại diện cho khối lượng bán tích lũy
- **Phân tích Thời gian**: Giới hạn bởi tính khả dụng và độ chi tiết của trường `date_created`
- **Ước tính Chi phí**: Tính toán ROI sử dụng giả định chi phí đơn giản hóa (60% doanh thu)
- **Tính mới của Dữ liệu**: Phân tích dựa trên dữ liệu snapshot mà không cập nhật thời gian thực
- **Phủ sóng Thị trường**: Phân tích giới hạn ở 6 danh mục sản phẩm

## Tính năng Phân tích Nâng cao

### 1. Phân tích Hiệu suất Kinh doanh

#### Nguyên tắc Pareto (Quy tắc 80/20)
- Xác định 20% sản phẩm hàng đầu tạo ra 80% bán hàng/đánh giá
- Phân tích cấp danh mục để tập trung chiến lược
- Giúp ưu tiên marketing và nỗ lực kho hàng

#### Phân tích Hiệu quả Giảm giá
- Tương quan phần trăm giảm giá với hiệu suất bán hàng
- Phân tích tác động lên chỉ số tương tác khách hàng
- Cung cấp insights cho tối ưu hóa chiến lược giá

#### Phân tích Thương hiệu
- So sánh hiệu suất giữa sản phẩm có thương hiệu vs không thương hiệu
- Tính chỉ số lợi thế thương hiệu (giá, đánh giá, khác biệt bán hàng)
- Xác định thương hiệu biểu diễn xuất sắc cho cơ hội hợp tác

### 2. Nâng cao Quản lý Kho hàng

#### Phân loại ABC
- **Danh mục A**: Sản phẩm giá trị cao (80% giá trị tích lũy hàng đầu) - Kiểm soát chặt chẽ
- **Danh mục B**: Sản phẩm giá trị trung bình (15% tiếp theo) - Kiểm soát vừa phải
- **Danh mục C**: Sản phẩm giá trị thấp (5% cuối) - Kiểm soát tối thiểu
- Cho phép chiến lược quản lý kho tập trung

#### Ước tính Rủi ro Hết hàng
- Sử dụng tốc độ bán và dữ liệu tuổi sản phẩm
- Phân loại sản phẩm thành Rủi ro Thấp/Trung bình/Cao
- Giúp ngăn ngừa mất bán hàng từ hết hàng

#### Lý luận SKU
- Xác định danh mục có quá nhiều sản phẩm biểu diễn thấp
- Khuyến nghị cơ hội giảm SKU
- Tối ưu hóa danh mục sản phẩm cho hiệu quả kho tốt hơn

### 3. Module Tiện ích Mới

#### metrics.py
- Hàm tính toán ROI
- Đánh giá sự hài lòng khách hàng
- Chỉ số luân chuyển kho
- Ước tính tỷ lệ chuyển đổi
- Tính toán độ co giãn giá

#### utils.py
- Xử lý và làm sạch văn bản tiếng Việt
- Định dạng tiền tệ (VND)
- Tiện ích xác thực dữ liệu
- Chức năng ghi log
- Phép toán toán học an toàn

#### dashboard.py (Tùy chọn)
- Dashboard Streamlit tương tác
- Trực quan hóa phân tích thời gian thực
- Insights cụ thể danh mục
- Giám sát chỉ số hiệu suất

## Quy trình Phân tích Nâng cao

### 1. Xử lý Dữ liệu Nâng cao
```python
from src.preprocessing import preprocess_data
df = preprocess_data()  # Bây giờ bao gồm đặc trưng mô tả và tính toán tuổi
```

### 2. Insights Hiệu suất
```python
from src.performance_analysis import analyze_pareto_principle, analyze_discount_effectiveness
pareto_results = analyze_pareto_principle(df)
discount_analysis = analyze_discount_effectiveness(df)
```

### 3. Tối ưu hóa Kho hàng
```python
from src.inventory_analysis import perform_abc_analysis, analyze_sku_rationalization
df_abc = perform_abc_analysis(df)
sku_recommendations = analyze_sku_rationalization(df)
```

### 4. Chỉ số Kinh doanh
```python
from src.metrics import calculate_roi, calculate_customer_satisfaction_score
roi = calculate_roi(revenue=1000000, cost=600000)  # 67% ROI
satisfaction = calculate_customer_satisfaction_score(rating=4.5, review_count=100)
```

## Insights Nâng cao Mẫu

Dựa trên phân tích 41.573 sản phẩm Tiki:

- **Phân loại ABC**: 2.252 mục A (5.4%), 4.657 mục B (11.2%), 34.664 mục C (83.4%)
- **Phân tích Pareto**: Nhiều danh mục tuân theo quy tắc 80/20 chặt chẽ
- **Tác động Giảm giá**: Tương quan vừa phải giữa mức giảm giá và khối lượng bán
- **Lợi thế Thương hiệu**: Sản phẩm có thương hiệu cho thấy lợi thế hiệu suất nhất quán
- **Cơ hội SKU**: Xác định danh mục có tiềm năng tối ưu hóa danh mục

## Chạy Dashboard

```bash
pip install streamlit
streamlit run src/dashboard.py
```

Dashboard cung cấp:
- Chỉ số hiệu suất tương tác
- Phân tích cụ thể danh mục
- Giám sát sức khỏe kho
- Trực quan hóa insights thời gian thực

## Đóng góp

Để đóng góp cho dự án này:
1. Tuân theo cấu trúc module trong `src/`
2. Thêm docstring toàn diện cho hàm mới
3. Cập nhật README này với tính năng và insights mới
4. Kiểm tra thay đổi trên dữ liệu mẫu trước khi commit

## Giấy phép

Dự án này dành cho mục đích giáo dục và phân tích. Vui lòng đảm bảo tuân thủ điều khoản dịch vụ và chính sách sử dụng dữ liệu của Tiki.
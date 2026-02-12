---
phase: design
title: System Design & Architecture
description: Define the technical architecture, components, and data models
---

# System Design & Architecture

## Architecture Overview
**What is the high-level system structure?**

- Include a mermaid diagram that captures the main components and their relationships. Example:
  ```mermaid
      graph LR
      subgraph Input
          A[Shopify Export File]
      end

      subgraph "Processing Logic"
          B[DF 1: Product Data]
          C[DF 2: Image URLs]
          
          B --- D{Match Logic}
          C --- D
          
          D --> E[Cleaned & Combined Dataset]
      end

      subgraph Output
          F[Final CSV]
          G[Final Excel]
      end

      A --> B
      A --> C
      E --> F
      E --> G
  ```
- Key components and their responsibilities
- Technology stack choices and rationale

## Data Models
**What data do we need to manage?**
- The only data source is an excel file from shopify. it will typically be called EB-Full-Backup-Export_{date}
- and the columns are: ID	Handle	Command	Title	Body HTML	Vendor	Type	Tags	Tags Command	Created At	Updated At	Status	Published	Published At	Published Scope	Template Suffix	Gift Card	URL	Total Inventory Qty	Row #	Top Row	Category: ID	Category: Name	Category	Custom Collections	Smart Collections	Image Type	Image Src	Image Command	Image Position	Image Width	Image Height	Image Alt Text	Variant Inventory Item ID	Variant ID	Variant Command	Option1 Name	Option1 Value	Option2 Name	Option2 Value	Option3 Name	Option3 Value	Variant Position	Variant SKU	Variant Barcode	Variant Image	Variant Weight	Variant Weight Unit	Variant Price	Variant Compare At Price	Variant Taxable	Variant Tax Code	Variant Inventory Tracker	Variant Inventory Policy	Variant Fulfillment Service	Variant Requires Shipping	Variant Inventory Qty	Variant Inventory Adjust	Variant Cost	Variant HS Code	Variant Country of Origin	Variant Province of Origin	Inventory Available: Sydney Warehouse	Inventory Available Adjust: Sydney Warehouse	Inventory On Hand: Sydney Warehouse	Inventory On Hand Adjust: Sydney Warehouse	Inventory Committed: Sydney Warehouse	Inventory Reserved: Sydney Warehouse	Inventory Damaged: Sydney Warehouse	Inventory Damaged Adjust: Sydney Warehouse	Inventory Safety Stock: Sydney Warehouse	Inventory Safety Stock Adjust: Sydney Warehouse	Inventory Quality Control: Sydney Warehouse	Inventory Quality Control Adjust: Sydney Warehouse	Inventory Incoming: Sydney Warehouse	Included / Australia	Price / Australia	Compare At Price / Australia	Included / new zealand	Price / new zealand	Compare At Price / new zealand	Metafield: title_tag [string]	Metafield: description_tag [string]	Metafield: shopify--discovery--product_search_boost.queries [list.single_line_text_field]	Metafield: shopify--discovery--product_recommendation.related_products [list.product_reference]	Metafield: shopify--discovery--product_recommendation.related_products_display [single_line_text_field]	Metafield: shopify--discovery--product_recommendation.complementary_products [list.product_reference]	Metafield: custom.brochure [file_reference]	Metafield: custom.size_range [single_line_text_field]	Metafield: custom.pms_colour [single_line_text_field]	Metafield: custom.gender [list.single_line_text_field]	Metafield: custom.gender_connection [product_reference]	Metafield: mm-google-shopping.custom_product [boolean]	Metafield: custom.portal_data [list.metaobject_reference]	Metafield: custom.chef_size_guide [file_reference]	Metafield: custom.bundle_products [list.product_reference]	Metafield: seo.hidden [number_integer]	Metafield: custom.hide_order_multiple_table [boolean]	Metafield: custom.size_helper_text [single_line_text_field]	Variant Metafield: custom.case_size [number_integer]	Variant Metafield: custom.product_status_ [list.single_line_text_field]	Variant Metafield: mm-google-shopping.age_group [single_line_text_field]	Variant Metafield: mm-google-shopping.condition [single_line_text_field]	Variant Metafield: mm-google-shopping.gender [single_line_text_field]	Variant Metafield: mm-google-shopping.mpn [single_line_text_field]	Variant Metafield: mm-google-shopping.size_type [single_line_text_field]	Variant Metafield: mm-google-shopping.size_system [single_line_text_field]	Variant Metafield: mm-google-shopping.custom_label_0 [single_line_text_field]	Variant Metafield: mm-google-shopping.custom_label_1 [single_line_text_field]	Variant Metafield: mm-google-shopping.custom_label_2 [single_line_text_field]	Variant Metafield: mm-google-shopping.custom_label_3 [single_line_text_field]	Variant Metafield: mm-google-shopping.custom_label_4 [single_line_text_field]	Variant Metafield: custom.all_colour [single_line_text_field]	Variant Metafield: custom._7_10_day_dispatch_stock [number_integer]	Variant Metafield: custom.pms [single_line_text_field]	Variant Metafield: custom.custom_portal_sku_s_ [mixed_reference]	Variant Metafield: custom.colour_swatch_url [single_line_text_field]	Variant Metafield: custom.product_status [single_line_text_field]	Variant Metafield: custom.netsuite_item_id [single_line_text_field]	Variant Metafield: custom.pms_colour [single_line_text_field]	Variant Metafield: custom.custom\.pms [single_line_text_field]	Variant Metafield: custom.custom\.pick_zone [single_line_text_field]	Variant Metafield: custom.pick_zone [single_line_text_field]	Metafield: custom.netsuite_item_id [single_line_text_field]	Metafield: custom.product_status [single_line_text_field]	Metafield: custom.case_size [number_integer]	Metafield: custom.custom\.pms [single_line_text_field]	Metafield: custom.pms [single_line_text_field]	Variant Metafield: custom.field_7_10_day_dispatch_stock [number_integer]	Variant Metafield: custom._field_7_10_day_dispatch_stock [number_integer]	Metafield: custom.pick_zone [single_line_text_field]	Variant Metafield: custom.colour_swatch [url]	Metafield: custom.custom\.pick_zone [single_line_text_field]	Metafield: custom.all_colour [single_line_text_field]	Metafield: custom._7_10_day_dispatch_stock [number_integer]	Metafield: mm-google-shopping.google_product_category [string]	Metafield: mc-facebook.google_product_category [string]	Metafield: custom.netsuite_item_id [integer]


## API Design
**How do components communicate?**
- Due to images not being linked to product variants, 2 data frames are created. One for variants, the other for images

## Component Breakdown
**What are the major building blocks?**
- a python script and input excel file

## Design Decisions
**Why did we choose this approach?**
- This is a first prototype, with a lofty end goal to fully automate the generation of this file

